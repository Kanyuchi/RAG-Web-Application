"""
API routes for query processing.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from datetime import datetime

from app.models.database import get_db
from app.models.query import Query, QueryStatus
from app.models.project import Project
from app.models.chunk import Chunk
from app.models.document import Document
from app.schemas.query import QueryRequest, QueryResponse
from app.core.logging import get_logger
from app.services.vector_db import vector_db
from app.services.llm import generate_rag_response

logger = get_logger(__name__)
router = APIRouter()


@router.get("/projects/{project_id}/queries", response_model=List[QueryResponse])
async def get_queries(project_id: str, db: Session = Depends(get_db)):
    """
    Get all queries for a project.
    """
    try:
        # Check if project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        queries = db.query(Query).filter(Query.project_id == project_id).order_by(Query.created_at).all()
        return queries

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching queries for project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch queries"
        )


@router.post("/queries", response_model=QueryResponse, status_code=status.HTTP_201_CREATED)
async def submit_query(
    query_request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a query and get RAG response.
    """
    try:
        # Check if project exists
        project = db.query(Project).filter(Project.id == query_request.project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        # Perform vector search to find relevant chunks
        logger.info(f"Searching for relevant chunks in project {query_request.project_id}")

        search_results = vector_db.search(
            query_text=query_request.query_text,
            project_id=query_request.project_id,
            top_k=query_request.top_k or 5,
            score_threshold=query_request.similarity_threshold or 0.7
        )

        if not search_results:
            logger.warning("No relevant chunks found for query")
            query_id = str(uuid4())
            response_text = "I couldn't find any relevant information in your documents to answer this question."
            citations = []
        else:
            # Get full chunk details from database
            chunk_ids = [result["chunk_id"] for result in search_results]
            chunks = db.query(Chunk).filter(Chunk.id.in_(chunk_ids)).all()
            chunks_dict = {chunk.id: chunk for chunk in chunks}

            # Get document details for citations
            doc_ids = list(set([result["document_id"] for result in search_results]))
            documents = db.query(Document).filter(Document.id.in_(doc_ids)).all()
            docs_dict = {doc.id: doc for doc in documents}

            # Prepare context for LLM
            context_chunks = []
            citations = []

            for i, result in enumerate(search_results):
                chunk = chunks_dict.get(result["chunk_id"])
                document = docs_dict.get(result["document_id"])

                if chunk and document:
                    context_chunks.append({
                        "text": chunk.content,
                        "score": result["score"],
                        "rank": i + 1
                    })

                    citations.append({
                        "chunk_id": chunk.id,
                        "document_id": document.id,
                        "document_name": document.filename,
                        "page_number": result.get("page_number"),
                        "similarity_score": result["score"],
                        "text": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
                    })

            # Generate response using LLM
            logger.info(f"Generating RAG response with {len(context_chunks)} chunks")

            try:
                response_text = generate_rag_response(
                    query=query_request.query_text,
                    context_chunks=context_chunks,
                    model=query_request.model or "gpt-4"
                )
            except Exception as e:
                logger.error(f"Error generating LLM response: {e}")
                response_text = f"Found relevant information but encountered an error generating the response: {str(e)}"

            query_id = str(uuid4())

        # Create query record
        db_query = Query(
            id=query_id,
            project_id=query_request.project_id,
            query_text=query_request.query_text,
            response_text=response_text,
            model_used=query_request.model or "gpt-4",
            citations=citations,
            status=QueryStatus.COMPLETED
        )

        db.add(db_query)

        # Update project query count
        project.query_count += 1

        db.commit()
        db.refresh(db_query)

        logger.info(f"Processed query for project {query_request.project_id}")
        return db_query

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process query"
        )


@router.get("/queries/{query_id}", response_model=QueryResponse)
async def get_query(query_id: str, db: Session = Depends(get_db)):
    """
    Get a specific query by ID.
    """
    try:
        query = db.query(Query).filter(Query.id == query_id).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Query not found"
            )
        return query

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching query {query_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch query"
        )
