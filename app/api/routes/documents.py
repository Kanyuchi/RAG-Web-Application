"""
API routes for document management.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
import os
import shutil

from app.models.database import get_db
from app.models.document import Document, DocumentStatus
from app.models.chunk import Chunk
from app.models.project import Project
from app.schemas.document import DocumentResponse
from app.core.config import settings
from app.core.logging import get_logger
from app.services.chunking import process_document
from app.services.vector_db import vector_db

logger = get_logger(__name__)
router = APIRouter()


@router.get("/projects/{project_id}/documents", response_model=List[DocumentResponse])
async def get_documents(project_id: str, db: Session = Depends(get_db)):
    """
    Get all documents for a project.
    """
    try:
        # Check if project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        documents = db.query(Document).filter(Document.project_id == project_id).all()
        return documents

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching documents for project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch documents"
        )


@router.post("/projects/{project_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document to a project.
    """
    try:
        # Check if project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        # Validate file type
        allowed_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "text/plain"
        ]

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not supported: {file.content_type}"
            )

        # Create upload directory if it doesn't exist
        upload_dir = settings.upload_dir
        os.makedirs(upload_dir, exist_ok=True)

        # Generate unique filename
        file_id = str(uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get file size
        file_size = os.path.getsize(file_path)

        # Validate file size
        if file_size > settings.max_file_size:
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size is {settings.max_file_size} bytes"
            )

        # Create document record
        db_document = Document(
            id=file_id,
            project_id=project_id,
            filename=file.filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file.content_type,
            status=DocumentStatus.UPLOADING,
            chunk_count=0
        )

        db.add(db_document)

        # Update project document count
        project.document_count += 1

        db.commit()
        db.refresh(db_document)

        logger.info(f"Uploaded document: {file.filename} to project {project_id}")

        # Process document: extract text, create chunks, and store vectors
        try:
            # Update status to processing
            db_document.status = DocumentStatus.PROCESSING
            db.commit()

            # Process document and create chunks
            chunks_data = process_document(file_path, file.content_type)
            logger.info(f"Created {len(chunks_data)} chunks from document")

            # Store chunks in database and vector database
            chunk_ids = []
            chunk_texts = []
            chunk_metadatas = []

            for chunk_data in chunks_data:
                # Create chunk record
                chunk = Chunk(
                    id=str(uuid4()),
                    document_id=file_id,
                    content=chunk_data["content"],
                    chunk_index=chunk_data["chunk_index"],
                    chunk_metadata={
                        "start_para": chunk_data.get("start_para"),
                        "end_para": chunk_data.get("end_para"),
                        "char_count": chunk_data.get("char_count")
                    },
                    parent_chunk_id=None
                )
                db.add(chunk)

                # Prepare for vector storage
                chunk_ids.append(chunk.id)
                chunk_texts.append(chunk.content)
                chunk_metadatas.append({
                    "document_id": file_id,
                    "project_id": project_id,
                    "filename": file.filename,
                    "chunk_index": chunk.chunk_index
                })

            # Store vectors in Qdrant
            if chunk_ids:
                vector_db.upsert_chunks(chunk_ids, chunk_texts, chunk_metadatas)
                logger.info(f"Stored {len(chunk_ids)} vectors in Qdrant")

            # Update document status and chunk count
            db_document.status = DocumentStatus.COMPLETED
            db_document.chunk_count = len(chunks_data)
            db_document.processed_at = db_document.uploaded_at  # Set processed time
            db.commit()
            db.refresh(db_document)

            logger.info(f"Successfully processed document: {file.filename}")

        except Exception as e:
            logger.error(f"Error processing document: {e}")
            db_document.status = DocumentStatus.FAILED
            db_document.error_message = str(e)
            db.commit()
            db.refresh(db_document)

        return db_document

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload document"
        )


@router.delete("/projects/{project_id}/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    project_id: str,
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a document from a project.
    """
    try:
        # Get document
        document = db.query(Document).filter(
            Document.id == document_id,
            Document.project_id == project_id
        ).first()

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Delete physical file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Get project to update count
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.document_count = max(0, project.document_count - 1)

        # Delete document record
        db.delete(document)
        db.commit()

        logger.info(f"Deleted document: {document_id} from project {project_id}")
        return None

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting document {document_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )
