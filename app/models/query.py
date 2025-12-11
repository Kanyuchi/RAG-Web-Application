"""
Query models - represents user queries and responses.
"""
from sqlalchemy import Column, String, DateTime, Text, Float, ForeignKey, Integer, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import uuid
import enum


class QueryStatus(str, enum.Enum):
    """Query processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Query(Base):
    """
    Query model for storing user queries.

    Each query belongs to a project and can have multiple associated chunks.
    """
    __tablename__ = "queries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)

    # Query information
    query_text = Column(Text, nullable=False)
    status = Column(Enum(QueryStatus), default=QueryStatus.PENDING, nullable=False, index=True)

    # Response information
    response_text = Column(Text, nullable=True)
    model_used = Column(String(100), nullable=True)  # 'openai' or 'anthropic'

    # Metadata
    processing_time = Column(Float, nullable=True)  # Time in seconds
    token_count = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)

    # Context and citations
    context_chunks_count = Column(Integer, default=0)
    citations = Column(JSON, nullable=True)  # Store citations as JSON array

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="queries")
    query_chunks = relationship("QueryChunk", back_populates="query", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Query(id={self.id}, project_id={self.project_id}, status={self.status})>"


class QueryChunk(Base):
    """
    Association table between queries and chunks.

    Stores which chunks were used for each query with relevance scores.
    """
    __tablename__ = "query_chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_id = Column(String, ForeignKey("queries.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_id = Column(String, ForeignKey("chunks.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relevance information
    similarity_score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)  # Rank in search results (1, 2, 3, ...)

    # Citation information
    used_in_response = Column(Integer, default=0)  # Boolean: was this chunk cited in response?
    citation_text = Column(Text, nullable=True)  # Specific text cited from chunk

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    query = relationship("Query", back_populates="query_chunks")
    chunk = relationship("Chunk", back_populates="queries")

    def __repr__(self):
        return f"<QueryChunk(query_id={self.query_id}, chunk_id={self.chunk_id}, score={self.similarity_score})>"
