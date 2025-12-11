"""
Project model - represents user projects.
"""
from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import uuid


class Project(Base):
    """
    Project model for storing user projects.

    Each project contains multiple documents and queries.
    """
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # User information (for future multi-user support)
    user_id = Column(String, nullable=True, index=True)

    # Statistics
    document_count = Column(Integer, default=0)
    query_count = Column(Integer, default=0)

    # Relationships
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    queries = relationship("Query", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name})>"
