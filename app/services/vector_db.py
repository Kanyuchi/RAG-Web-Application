"""
Qdrant vector database client for semantic search.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import numpy as np

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorDatabase:
    """
    Qdrant vector database client for storing and searching document embeddings.
    """

    def __init__(self):
        """Initialize Qdrant client and embedding model."""
        self.client = None
        self.embedding_model = None
        self.collection_name = settings.qdrant_collection_name
        self.embedding_dimension = settings.embedding_dimension

    def connect(self) -> bool:
        """
        Connect to Qdrant and initialize embedding model.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Initialize Qdrant client
            if settings.qdrant_url:
                # Use cloud/remote Qdrant
                self.client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key
                )
            else:
                # Use local Qdrant
                self.client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port
                )

            # Load embedding model
            logger.info(f"Loading embedding model: {settings.embedding_model}")
            self.embedding_model = SentenceTransformer(settings.embedding_model)

            # Verify dimension matches
            test_embedding = self.embedding_model.encode(["test"])
            actual_dimension = len(test_embedding[0])
            if actual_dimension != settings.embedding_dimension:
                logger.warning(
                    f"Embedding dimension mismatch: config={settings.embedding_dimension}, "
                    f"actual={actual_dimension}. Updating to actual dimension."
                )
                self.embedding_dimension = actual_dimension

            logger.info("Vector database connected successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to vector database: {e}")
            return False

    def create_collection(self, recreate: bool = False) -> bool:
        """
        Create collection in Qdrant if it doesn't exist.

        Args:
            recreate: If True, delete existing collection and recreate

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get list of collections
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]

            if recreate and self.collection_name in collection_names:
                logger.info(f"Deleting existing collection: {self.collection_name}")
                self.client.delete_collection(self.collection_name)
                collection_names.remove(self.collection_name)

            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dimension,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection created: {self.collection_name}")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            return False

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        if self.embedding_model is None:
            raise RuntimeError("Embedding model not initialized. Call connect() first.")

        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        if self.embedding_model is None:
            raise RuntimeError("Embedding model not initialized. Call connect() first.")

        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def upsert_chunks(
        self,
        chunk_ids: List[str],
        texts: List[str],
        metadatas: List[Dict[str, Any]]
    ) -> bool:
        """
        Insert or update document chunks with embeddings.

        Args:
            chunk_ids: List of chunk IDs
            texts: List of chunk texts
            metadatas: List of metadata dicts for each chunk

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Upserting {len(chunk_ids)} chunks to vector database")

            # Generate embeddings
            embeddings = self.generate_embeddings_batch(texts)

            # Create points
            points = [
                PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "text": text,
                        **metadata
                    }
                )
                for chunk_id, embedding, text, metadata in zip(
                    chunk_ids, embeddings, texts, metadatas
                )
            ]

            # Upsert to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully upserted {len(chunk_ids)} chunks")
            return True

        except Exception as e:
            logger.error(f"Failed to upsert chunks: {e}")
            return False

    def search(
        self,
        query_text: str,
        project_id: Optional[str] = None,
        document_id: Optional[str] = None,
        top_k: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks.

        Args:
            query_text: Query text
            project_id: Filter by project ID
            document_id: Filter by document ID
            top_k: Number of results to return
            score_threshold: Minimum similarity score

        Returns:
            List of search results with scores and metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.generate_embedding(query_text)

            # Build filter
            query_filter = None
            conditions = []

            if project_id:
                conditions.append(
                    FieldCondition(
                        key="project_id",
                        match=MatchValue(value=project_id)
                    )
                )

            if document_id:
                conditions.append(
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id)
                    )
                )

            if conditions:
                query_filter = Filter(must=conditions)

            # Search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=query_filter,
                limit=top_k,
                score_threshold=score_threshold
            )

            # Format results
            results = []
            for i, hit in enumerate(search_results):
                results.append({
                    "chunk_id": hit.id,
                    "score": hit.score,
                    "rank": i + 1,
                    "text": hit.payload.get("text", ""),
                    "document_id": hit.payload.get("document_id"),
                    "project_id": hit.payload.get("project_id"),
                    "page_number": hit.payload.get("page_number"),
                    "metadata": hit.payload
                })

            logger.info(f"Found {len(results)} results for query")
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def delete_chunks(self, chunk_ids: List[str]) -> bool:
        """
        Delete chunks from vector database.

        Args:
            chunk_ids: List of chunk IDs to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=chunk_ids
                )
            )
            logger.info(f"Deleted {len(chunk_ids)} chunks from vector database")
            return True

        except Exception as e:
            logger.error(f"Failed to delete chunks: {e}")
            return False

    def delete_by_document(self, document_id: str) -> bool:
        """
        Delete all chunks for a document.

        Args:
            document_id: Document ID

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=Filter(
                        must=[
                            FieldCondition(
                                key="document_id",
                                match=MatchValue(value=document_id)
                            )
                        ]
                    )
                )
            )
            logger.info(f"Deleted all chunks for document: {document_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete document chunks: {e}")
            return False


# Global vector database instance
vector_db = VectorDatabase()
