"""
Pydantic schemas for Project endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base schema for Project."""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    user_id: Optional[str] = Field(None, description="User ID (for multi-user support)")


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    id: str
    user_id: Optional[str]
    document_count: int = 0
    query_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for listing projects."""
    projects: list[ProjectResponse]
    total: int
