"""
FastAPI main application for RAG Web Application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import get_logger
from app.models.database import check_db_connection, init_db
from app.services.vector_db import vector_db

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info("=" * 60)

    # Check database connections
    logger.info("Checking database connections...")
    if check_db_connection():
        logger.info("PostgreSQL connection: OK")
    else:
        logger.error("PostgreSQL connection: FAILED")

    # Connect to vector database
    if vector_db.connect():
        logger.info("Qdrant connection: OK")
        # Ensure collection exists
        vector_db.create_collection(recreate=False)
    else:
        logger.error("Qdrant connection: FAILED")

    logger.info("Application started successfully")
    logger.info(f"API Documentation: http://{settings.host}:{settings.port}/docs")
    logger.info("=" * 60)

    yield

    # Shutdown
    logger.info("Shutting down application...")
    logger.info("Application stopped")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Retrieval-Augmented Generation (RAG) Web Application with hierarchical chunking and semantic search",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    db_status = check_db_connection()

    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "vector_db": "connected",  # Assume connected if app started
        "version": settings.app_version
    }


# Import and include API routers
from app.api.routes import projects, documents, queries

app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(documents.router, prefix="", tags=["documents"])
app.include_router(queries.router, prefix="", tags=["queries"])
