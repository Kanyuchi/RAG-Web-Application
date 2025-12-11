"""
Test script to verify all components are working.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.models import check_db_connection
from app.services.vector_db import vector_db
from app.core.logging import logger


def test_configuration():
    """Test configuration loading."""
    logger.info("\n1. Testing Configuration...")
    try:
        logger.info(f"  App Name: {settings.app_name}")
        logger.info(f"  App Version: {settings.app_version}")
        logger.info(f"  Debug Mode: {settings.debug}")
        logger.info(f"  Database URL: {settings.database_url[:30]}...")
        logger.info(f"  Qdrant Host: {settings.qdrant_host}:{settings.qdrant_port}")
        logger.info(f"  Embedding Model: {settings.embedding_model}")
        logger.info(f"  OpenAI API Key: {'Set' if settings.openai_api_key else 'Not set'}")
        logger.info(f"  Anthropic API Key: {'Set' if settings.anthropic_api_key else 'Not set'}")
        logger.info("  ✓ Configuration loaded successfully")
        return True
    except Exception as e:
        logger.error(f"  ✗ Configuration error: {e}")
        return False


def test_database():
    """Test PostgreSQL connection."""
    logger.info("\n2. Testing PostgreSQL Connection...")
    if check_db_connection():
        logger.info("  ✓ PostgreSQL connection successful")
        return True
    else:
        logger.error("  ✗ PostgreSQL connection failed")
        return False


def test_vector_db():
    """Test Qdrant connection."""
    logger.info("\n3. Testing Qdrant Vector Database...")
    if vector_db.connect():
        logger.info("  ✓ Qdrant connection successful")

        # Test embedding generation
        try:
            test_text = "This is a test sentence for embedding generation."
            embedding = vector_db.generate_embedding(test_text)
            logger.info(f"  ✓ Embedding generated (dimension: {len(embedding)})")
            return True
        except Exception as e:
            logger.error(f"  ✗ Embedding generation failed: {e}")
            return False
    else:
        logger.error("  ✗ Qdrant connection failed")
        return False


def test_directories():
    """Test directory creation."""
    logger.info("\n4. Testing Directory Structure...")
    try:
        upload_dir = settings.upload_path
        processed_dir = settings.processed_path

        logger.info(f"  Upload Directory: {upload_dir}")
        logger.info(f"  Processed Directory: {processed_dir}")
        logger.info(f"  ✓ Directories exist and are accessible")
        return True
    except Exception as e:
        logger.error(f"  ✗ Directory error: {e}")
        return False


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("RAG APPLICATION SETUP TEST")
    logger.info("=" * 60)

    results = []
    results.append(("Configuration", test_configuration()))
    results.append(("PostgreSQL", test_database()))
    results.append(("Qdrant", test_vector_db()))
    results.append(("Directories", test_directories()))

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"  {test_name}: {status}")
        if not passed:
            all_passed = False

    logger.info("=" * 60)

    if all_passed:
        logger.info("\n✓ ALL TESTS PASSED - Setup is complete!")
        logger.info("\nNext steps:")
        logger.info("  1. Run: python scripts/init_db.py (if not done)")
        logger.info("  2. Start app: uvicorn app.main:app --reload")
    else:
        logger.error("\n✗ SOME TESTS FAILED - Please fix the issues above")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
