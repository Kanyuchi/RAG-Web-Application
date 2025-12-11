"""
Document model - represents uploaded documents.
"""
from sqlalchemy import Column, String, DateTime, Text, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import uuid
import enum


class DocumentStatus(str, enum.Enum):
    """Document processing status."""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base):
    """
    Document model for storing uploaded files metadata.

    Each document belongs to a project and contains multiple chunks.
    """
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)

    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_type = Column(String(50), nullable=False)  # e.g., 'application/pdf'
    mime_type = Column(String(100), nullable=True)

    # Processing information
    status = Column(Enum(DocumentStatus), default=DocumentStatus.UPLOADING, nullable=False, index=True)
    processing_error = Column(Text, nullable=True)

    # Content metadata
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    chunk_count = Column(Integer, default=0)

    # Source information (for Google Drive integration)
    source = Column(String(50), default="upload")  # 'upload' or 'google_drive'
    source_url = Column(String(500), nullable=True)
    source_id = Column(String(255), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, status={self.status})>"
