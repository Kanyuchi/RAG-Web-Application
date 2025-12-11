"""
Pydantic schemas for Query endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.query import QueryStatus


class Citation(BaseModel):
    """Schema for citation information."""
    chunk_id: str
    document_id: str
    document_name: str
    page_number: Optional[int]
    similarity_score: float
    text: str
    rank: int


class QueryRequest(BaseModel):
    """Schema for submitting a query."""
    query_text: str = Field(..., min_length=1, description="User's question")
    model: Optional[str] = Field(default="openai", description="LLM provider: 'openai' or 'anthropic'")
    max_chunks: Optional[int] = Field(default=5, ge=1, le=20, description="Maximum chunks to retrieve")


class QueryResponse(BaseModel):
    """Schema for query response."""
    id: str
    project_id: str
    query_text: str
    response_text: Optional[str]
    status: QueryStatus
    model_used: Optional[str]
    processing_time: Optional[float]
    citations: Optional[List[Citation]]
    context_chunks_count: int
    created_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]

    class Config:
        from_attributes = True


class QueryHistoryResponse(BaseModel):
    """Schema for query history."""
    queries: List[QueryResponse]
    total: int


class QueryDetailResponse(BaseModel):
    """Schema for detailed query response with full context."""
    id: str
    project_id: str
    query_text: str
    response_text: Optional[str]
    status: QueryStatus
    model_used: Optional[str]
    processing_time: Optional[float]
    token_count: Optional[int]
    citations: Optional[List[Citation]]
    context_chunks_count: int
    created_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]

    class Config:
        from_attributes = True
