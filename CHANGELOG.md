# Changelog

All notable changes to the RAG Web Application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- API routes for project management
- Document upload and processing pipeline
- RAG query processing with citations
- Frontend UI implementation
- Google Drive integration
- Authentication and authorization
- Comprehensive testing suite

---

## [1.0.0] - 2025-11-04

### Added - Phase 1: Core Infrastructure

#### Configuration & Setup
- Core configuration system using Pydantic Settings
- Environment variable management via `.env` file
- Centralized logging configuration with file and console output
- Docker Compose setup for PostgreSQL and Qdrant
- Comprehensive project documentation

#### Database Architecture
- **PostgreSQL Models** (SQLAlchemy):
  - `Project` model for user projects
  - `Document` model for uploaded file metadata
  - `Chunk` model for document chunks with hierarchical structure
  - `Query` model for user queries with responses
  - `QueryChunk` association model for query-chunk relationships with scores
- Database connection management with pooling
- Automatic timezone handling (UTC)
- Database initialization scripts

#### Vector Database Integration
- Qdrant client implementation for semantic search
- Sentence-transformers integration (`all-MiniLM-L6-v2`)
- 384-dimensional vector embeddings
- Collection management and CRUD operations
- Batch embedding processing
- Similarity search with project/document filtering

#### API Framework
- FastAPI application setup with automatic documentation
- CORS middleware configuration
- Health check endpoint
- Lifespan events for startup/shutdown
- **Pydantic Schemas**:
  - Project schemas (create, update, response)
  - Document schemas (upload, status, response)
  - Query schemas (request, response with citations)

#### Development Tools
- Virtual environment setup
- Dependencies management (`requirements.txt`)
- Database initialization script (`scripts/init_db.py`)
- Setup verification script (`scripts/test_setup.py`)
- Playwright MCP configuration for browser automation

#### Documentation
- Comprehensive README with setup instructions
- Development roadmap (`docs/DEVELOPMENT_ROADMAP.md`)
- Setup completion guide (`docs/SETUP_COMPLETE.md`)
- Playwright MCP setup guide (`docs/PLAYWRIGHT_MCP_SETUP.md`)
- Next steps guide (`NEXT_STEPS.md`)
- This CHANGELOG file
- CLAUDE.md for AI assistant context

### Fixed
- SQLAlchemy 2.0 compatibility with `text()` wrapper for raw SQL
- Reserved keyword conflict (`metadata` → `chunk_metadata`)
- Qdrant client API compatibility (`collection_exists` → `get_collections`)
- Sentence-transformers version incompatibility (upgraded to 5.1.0+)
- PostgreSQL connection configuration for local database

### Technical Details

**Technologies Used:**
- **Backend**: Python 3.11+, FastAPI 0.104.1
- **Database**: PostgreSQL 15 (local)
- **Vector DB**: Qdrant (Docker)
- **Embeddings**: Sentence-transformers 5.1.0+
- **LLM APIs**: OpenAI GPT-4, Anthropic Claude 3.5 Sonnet
- **Development**: Docker, pytest, black, flake8

**Database Schema:**
```
projects (id, name, description, user_id, document_count, query_count, timestamps)
  ├── documents (id, project_id, file metadata, processing status, timestamps)
  │    └── chunks (id, document_id, content, hierarchical info, vector_id, timestamps)
  └── queries (id, project_id, query_text, response_text, model_used, citations, timestamps)
       └── query_chunks (id, query_id, chunk_id, similarity_score, rank, citation_text)
```

**Vector Database:**
- Collection: `rag_documents`
- Dimensions: 384
- Distance metric: Cosine similarity
- Model: `all-MiniLM-L6-v2`

### Development Stats
- **Files Created**: 50+
- **Lines of Code**: 3000+
- **Models**: 5 SQLAlchemy models
- **Schemas**: 9 Pydantic schemas
- **Services**: 5 core services
- **Documentation**: 7 comprehensive guides

---

## Development Guidelines

### Version Numbering
- **Major** (X.0.0): Breaking changes or major feature releases
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, minor improvements

### Changelog Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

### How to Update This Changelog
1. Always update BEFORE making significant changes
2. Add entries under `[Unreleased]` section
3. Move entries to a new version section on release
4. Include date in ISO format (YYYY-MM-DD)
5. Link version numbers to release tags
6. Keep entries concise but descriptive

### Example Entry Format
```markdown
### Added
- Feature description with implementation details
  - Sub-feature or technical detail
  - File location: `path/to/file.py:123`
```

---

## Links
- [Repository](https://github.com/yourusername/rag-app)
- [Documentation](./README.md)
- [Development Roadmap](./docs/DEVELOPMENT_ROADMAP.md)
- [Issues](https://github.com/yourusername/rag-app/issues)

---

*Last Updated: 2025-11-04*
*Maintained by: Development Team*
