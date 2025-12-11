"""
Pydantic schemas for Document endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.document import DocumentStatus


class DocumentBase(BaseModel):
    """Base schema for Document."""
    filename: str
    file_size: int
    file_type: str


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    id: str
    project_id: str
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    status: DocumentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    """Schema for document response with full details."""
    id: str
    project_id: str
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str
    status: DocumentStatus
    processing_error: Optional[str]
    page_count: Optional[int]
    word_count: Optional[int]
    chunk_count: int
    source: str
    source_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for listing documents."""
    documents: list[DocumentResponse]
    total: int


class DocumentStatusResponse(BaseModel):
    """Schema for document processing status."""
    id: str
    status: DocumentStatus
    processing_error: Optional[str]
    chunk_count: int
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


class GoogleDriveAttachRequest(BaseModel):
    """Schema for attaching Google Drive files."""
    google_drive_link: str = Field(..., description="Google Drive file or folder link")
