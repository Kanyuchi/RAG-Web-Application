"""
Chunk model - represents document chunks with embeddings.
"""
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import uuid


class Chunk(Base):
    """
    Chunk model for storing document chunks.

    Each chunk is a segment of a document with its embedding stored in Qdrant.
    This model stores metadata and references to the vector database.
    """
    __tablename__ = "chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)

    # Chunk content
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)  # Position in document

    # Hierarchical information
    level = Column(String(50), nullable=True)  # 'chapter', 'section', 'paragraph'
    parent_chunk_id = Column(String, ForeignKey("chunks.id"), nullable=True)

    # Source information
    page_number = Column(Integer, nullable=True)
    start_char = Column(Integer, nullable=True)
    end_char = Column(Integer, nullable=True)

    # Metadata (using chunk_metadata to avoid SQLAlchemy reserved name)
    chunk_metadata = Column(JSON, nullable=True)  # Store additional metadata as JSON
    word_count = Column(Integer, nullable=True)

    # Vector database reference
    vector_id = Column(String, nullable=True, index=True)  # ID in Qdrant
    embedding_model = Column(String(100), nullable=True)  # Model used for embedding

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    document = relationship("Document", back_populates="chunks")
    queries = relationship("QueryChunk", back_populates="chunk")

    def __repr__(self):
        return f"<Chunk(id={self.id}, document_id={self.document_id}, index={self.chunk_index})>"
