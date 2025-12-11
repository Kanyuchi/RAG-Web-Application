"""
Database initialization script.
Creates all tables and sets up vector database.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import init_db, check_db_connection
from app.services.vector_db import vector_db
from app.core.logging import logger


def main():
    """Initialize databases."""
    logger.info("=" * 60)
    logger.info("DATABASE INITIALIZATION")
    logger.info("=" * 60)

    # Check PostgreSQL connection
    logger.info("\n1. Checking PostgreSQL connection...")
    if check_db_connection():
        logger.info("✓ PostgreSQL connection successful")
    else:
        logger.error("✗ PostgreSQL connection failed")
        logger.error("Please check your DATABASE_URL in .env file")
        return False

    # Initialize tables
    logger.info("\n2. Creating database tables...")
    try:
        init_db()
        logger.info("✓ Database tables created successfully")
    except Exception as e:
        logger.error(f"✗ Failed to create tables: {e}")
        return False

    # Connect to Qdrant
    logger.info("\n3. Connecting to Qdrant vector database...")
    if vector_db.connect():
        logger.info("✓ Qdrant connection successful")
    else:
        logger.error("✗ Qdrant connection failed")
        logger.error("Please check your QDRANT settings in .env file")
        return False

    # Create collection
    logger.info("\n4. Creating Qdrant collection...")
    if vector_db.create_collection(recreate=False):
        logger.info("✓ Qdrant collection ready")
    else:
        logger.error("✗ Failed to create Qdrant collection")
        return False

    logger.info("\n" + "=" * 60)
    logger.info("✓ DATABASE INITIALIZATION COMPLETE")
    logger.info("=" * 60)
    logger.info("\nYou can now start the application with:")
    logger.info("  uvicorn app.main:app --reload")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
