# RAG Web Application - Claude Code Context

> **Purpose**: This document provides context for Claude Code (and other AI assistants) working on this project.
> Always read this file before making changes or suggestions.

---

## Project Overview

**Name**: RAG Web Application
**Version**: 1.0.0
**Status**: Phase 1 Complete (Core Infrastructure) ✅
**Started**: 2025-11-04

### What This Project Does

This is a **Retrieval-Augmented Generation (RAG)** web application that enables users to:
1. Upload PDFs or attach files from Google Drive to projects
2. Automatically chunk documents using hierarchical methods
3. Query their documents using natural language
4. Receive AI-generated responses with citations and relevance scores
5. Maintain full conversation history for auditing

### Key Features
- **Project-based workspace** for document organization
- **Hierarchical chunking** (chapter → section → paragraph)
- **Semantic search** using vector embeddings (384-dim, all-MiniLM-L6-v2)
- **Dual LLM support** (OpenAI GPT-4, Anthropic Claude 3.5 Sonnet)
- **Citation tracking** with relevance scores
- **Continuous logging** of all queries and responses

---

## Architecture

### Technology Stack

**Backend:**
- Python 3.11+
- FastAPI 0.104.1
- SQLAlchemy 2.0.23 (ORM)
- Pydantic 2.5.0 (validation)

**Databases:**
- PostgreSQL 15 (structured data) - Local on port 5432
- Qdrant (vector embeddings) - Docker on ports 6333-6334

**AI/ML:**
- Sentence-transformers 5.1.0+ (embeddings)
- OpenAI API (GPT-4)
- Anthropic API (Claude 3.5 Sonnet)

**Frontend** (Planned):
- Next.js / React
- TailwindCSS
- TypeScript

### Project Structure

```
Rag_App/
├── app/
│   ├── main.py              # ✅ FastAPI app with lifespan events
│   ├── core/                # ✅ Configuration & logging
│   │   ├── config.py        # Pydantic Settings
│   │   └── logging.py       # Logging setup
│   ├── models/              # ✅ SQLAlchemy models (5 models)
│   │   ├── database.py      # DB connection
│   │   ├── project.py
│   │   ├── document.py
│   │   ├── chunk.py
│   │   └── query.py
│   ├── schemas/             # ✅ Pydantic schemas (9 schemas)
│   │   ├── project.py
│   │   ├── document.py
│   │   └── query.py
│   ├── services/            # ✅ Business logic
│   │   ├── vector_db.py     # Qdrant client
│   │   ├── chunking.py      # ⏳ Stub (needs implementation)
│   │   ├── llm_openai.py    # ⏳ Stub (needs implementation)
│   │   ├── llm_anthropic.py # ⏳ Stub (needs implementation)
│   │   └── storage.py       # ⏳ Stub (needs implementation)
│   ├── api/routes/          # ⏳ To be created
│   └── utils/               # ⏳ To be created
├── scripts/
│   ├── init_db.py          # ✅ Database initialization
│   └── test_setup.py       # ✅ Setup verification
├── data/
│   ├── uploads/            # File uploads
│   └── processed/          # Processed data
├── tests/                  # ⏳ To be created
├── frontend/               # ⏳ To be created
├── docs/                   # ✅ Comprehensive documentation
├── .env                    # ✅ Environment variables (with API keys)
├── .mcp.json               # ✅ Playwright MCP config
├── docker-compose.yml      # ✅ Qdrant setup
├── requirements.txt        # ✅ Python dependencies
├── CHANGELOG.md            # ✅ Version history
└── README.md               # ✅ Project documentation
```

---

## Database Schema

### PostgreSQL Tables (all created ✅)

**projects**
- Primary workspace entity
- Tracks document and query counts
- Fields: id, name, description, user_id, timestamps

**documents**
- Uploaded file metadata
- Processing status tracking
- Fields: id, project_id, filename, file_size, file_type, status, page_count, chunk_count, timestamps

**chunks**
- Document segments with hierarchical structure
- Links to vector database
- Fields: id, document_id, content, chunk_index, level, parent_chunk_id, page_number, chunk_metadata, vector_id, timestamps

**queries**
- User questions and AI responses
- Fields: id, project_id, query_text, response_text, model_used, processing_time, citations, timestamps

**query_chunks**
- Association table linking queries to chunks
- Fields: id, query_id, chunk_id, similarity_score, rank, used_in_response, citation_text

### Qdrant Collection

**Name**: `rag_documents`
**Dimensions**: 384
**Distance**: Cosine similarity
**Status**: ✅ Created and ready

---

## Environment & Configuration

### Database Credentials
- **PostgreSQL**:
  - Host: 127.0.0.1:5432
  - Database: rag_db
  - User: postgres
  - Password: dbi021224 (stored in `.env`)

- **Qdrant**:
  - Host: localhost:6333 (Docker)
  - Collection: rag_documents

### API Keys (in `.env`)
- `OPENAI_API_KEY`: Configured ✅
- `ANTHROPIC_API_KEY`: Configured ✅
- `FIRECRAWL_API_KEY`: Configured ✅
- `PERPLEXITY_API_KEY`: Configured ✅

### MCP Servers Available
- `DBI_Strategy_DB` - Business data
- `DBI_DATA` - Population & property data
- `postgres` - Economic sector data
- `perplexity` - Web search capabilities
- `playwright` (configured but needs Docker Desktop restart)

---

## Current Status

### ✅ Completed (Phase 1)
- [x] Core configuration system
- [x] Logging infrastructure
- [x] Database models (5 models)
- [x] API schemas (9 schemas)
- [x] PostgreSQL connection & tables
- [x] Qdrant vector database setup
- [x] Sentence-transformers integration
- [x] Main FastAPI app with lifespan events
- [x] Docker Compose configuration
- [x] Initialization scripts
- [x] Comprehensive documentation

### ⏳ In Progress (Phase 2)
- [ ] API routes (projects, documents, queries)
- [ ] Document processing pipeline
- [ ] Advanced chunking implementation
- [ ] LLM integration enhancement
- [ ] Frontend UI

### 📋 Planned (Phase 3+)
- [ ] Query processing with RAG
- [ ] Citation extraction
- [ ] Google Drive integration
- [ ] Authentication
- [ ] Testing suite
- [ ] Deployment configuration

---

## Development Guidelines

### When Making Changes

1. **Always check CHANGELOG.md first**
   - See what's been done
   - Understand recent changes
   - Plan your updates

2. **Update CHANGELOG.md**
   - Add entry under `[Unreleased]`
   - Describe what you're adding/changing
   - Include file locations

3. **Follow existing patterns**
   - Check similar implementations first
   - Maintain consistent code style
   - Use existing services/utilities

4. **Test database changes**
   - Run `scripts/test_setup.py` after changes
   - Verify migrations if schema changes
   - Check both PostgreSQL and Qdrant

5. **Update documentation**
   - Update README.md if user-facing
   - Update this file (CLAUDE.md) if architecture changes
   - Add comments to complex code

### Code Style
- Use **type hints** everywhere
- Follow **PEP 8** (use `black` formatter)
- Add **docstrings** to all functions/classes
- Use **async/await** for I/O operations
- Handle **exceptions** gracefully with logging

### Common Patterns

**Adding a new model:**
1. Create in `app/models/`
2. Import in `app/models/__init__.py`
3. Create corresponding schema in `app/schemas/`
4. Update `scripts/init_db.py` if needed

**Adding a new API route:**
1. Create in `app/api/routes/`
2. Use dependency injection: `db: Session = Depends(get_db)`
3. Use Pydantic schemas for validation
4. Include in `app/main.py` with `app.include_router()`

**Adding a new service:**
1. Create in `app/services/`
2. Use `get_logger(__name__)` for logging
3. Handle errors and log them
4. Write docstrings with examples

---

## Known Issues & Limitations

### Technical Debt
1. **Unicode logging on Windows**: Console logging has encoding issues with checkmarks (✓/✗)
   - Doesn't affect functionality
   - Only cosmetic issue in logs

2. **Stub implementations**: Several services need full implementation:
   - `services/chunking.py` - Basic stub, needs hierarchical logic
   - `services/llm_*.py` - Basic stubs, need proper prompts
   - `services/storage.py` - Basic stub, needs full implementation

3. **No authentication yet**: All endpoints are public
   - Planned for later phase
   - Consider for multi-user deployment

### Environment-Specific
- **PostgreSQL**: Using local instance (not Docker)
- **Port 5432**: Local PostgreSQL conflicts with Docker
- **Qdrant**: Running in Docker on 6333

---

## Testing

### Manual Testing
```bash
# 1. Test setup
python scripts/test_setup.py

# 2. Start application
uvicorn app.main:app --reload

# 3. Check health
curl http://localhost:8000/health

# 4. View API docs
open http://localhost:8000/docs
```

### Automated Testing (To be implemented)
```bash
pytest tests/
pytest tests/ --cov=app
```

---

## Deployment Notes

### Development
- Uses local PostgreSQL on port 5432
- Qdrant in Docker
- Hot reload enabled (`--reload`)

### Production (Future)
- Will need Docker for both databases
- Environment-specific `.env` files
- Proper secret management
- Load balancing for FastAPI

---

## API Endpoints (Current)

```
GET  /           - API information
GET  /health     - Health check
GET  /docs       - Swagger UI documentation
GET  /redoc      - ReDoc documentation
```

### Planned Endpoints
```
POST   /projects              - Create project
GET    /projects              - List projects
GET    /projects/{id}         - Get project
DELETE /projects/{id}         - Delete project

POST   /projects/{id}/upload  - Upload documents
GET    /projects/{id}/documents - List documents
DELETE /documents/{id}        - Delete document

POST   /projects/{id}/query   - Submit query
GET    /projects/{id}/history - Get query history
```

---

## Useful Commands

```bash
# Activate environment
.\venv\Scripts\activate

# Start application
uvicorn app.main:app --reload

# Initialize database
python scripts/init_db.py

# Run tests
pytest tests/

# Format code
black app/

# Lint code
flake8 app/

# Database operations
docker-compose up -d       # Start databases
docker-compose down        # Stop databases
docker ps                  # Check running containers
```

---

## External Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy**: https://docs.sqlalchemy.org
- **Qdrant**: https://qdrant.tech/documentation
- **Sentence-transformers**: https://www.sbert.net

---

## Change Log for This File

- **2025-11-04**: Initial creation with Phase 1 completion status
  - Added complete project overview
  - Documented architecture and current status
  - Added development guidelines
  - Linked to CHANGELOG.md

---

*Last Updated: 2025-11-04 22:35 UTC*
*For version history, always check CHANGELOG.md*
*This file should be updated whenever architecture changes*
