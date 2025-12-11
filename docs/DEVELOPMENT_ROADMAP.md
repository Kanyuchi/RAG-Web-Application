# RAG Application Development Roadmap

## Current Status

### ✅ Completed
- Project structure initialized
- Directory organization complete
- Dependencies defined in `requirements.txt`
- Environment variables configured (`.env` with API keys)
- Playwright MCP configured for testing
- Basic service stubs created:
  - `services/chunking.py` - Hierarchical chunking stub
  - `services/llm_openai.py` - OpenAI integration stub
  - `services/llm_anthropic.py` - Anthropic integration stub
  - `services/storage.py` - Query storage stub
- Basic FastAPI app structure in `main.py`

### 🚧 Current State
We have a skeleton project with basic stubs. Need to implement:
1. Core configuration system
2. Database models
3. Vector database integration
4. Complete document processing pipeline
5. Full API endpoints
6. Authentication (if needed)

---

## Phase 1: Core Infrastructure (Current Phase)

### Step 1.1: Core Configuration & Settings ⏳
**File**: `app/core/config.py`

**Purpose**: Centralize all configuration using Pydantic Settings

**Tasks**:
- [ ] Load environment variables
- [ ] Define app settings (database URLs, API keys, etc.)
- [ ] Configure logging
- [ ] Set up CORS and security settings

**Files to create**:
- `app/core/config.py`
- `app/core/logging.py`
- `app/core/security.py` (optional for now)

### Step 1.2: Database Models & Schemas
**Files**: `app/models/*.py`

**Purpose**: Define data structures for PostgreSQL

**Models needed**:
- [ ] `Project` - User projects
- [ ] `Document` - Uploaded documents metadata
- [ ] `Chunk` - Document chunks with embeddings
- [ ] `Query` - User queries
- [ ] `QueryResponse` - Query responses with citations

**Schemas needed** (Pydantic):
- [ ] Request/Response schemas for API validation

**Files to create**:
- `app/models/database.py` - SQLAlchemy setup
- `app/models/project.py`
- `app/models/document.py`
- `app/models/chunk.py`
- `app/models/query.py`
- `app/schemas/project.py` - Pydantic schemas
- `app/schemas/document.py`
- `app/schemas/query.py`

### Step 1.3: Vector Database Integration (Qdrant)
**File**: `app/services/vector_db.py`

**Purpose**: Connect to Qdrant for semantic search

**Tasks**:
- [ ] Initialize Qdrant client
- [ ] Create collections
- [ ] Implement embedding generation (sentence-transformers)
- [ ] Implement vector upsert
- [ ] Implement similarity search

---

## Phase 2: Document Processing Pipeline

### Step 2.1: Document Ingestion
**File**: `app/services/document_processor.py`

**Tasks**:
- [ ] PDF text extraction (PyPDF2/pdfplumber)
- [ ] Table extraction from PDFs
- [ ] Document metadata extraction
- [ ] File validation and sanitization

### Step 2.2: Advanced Chunking Implementation
**File**: `app/services/chunking.py` (enhance existing)

**Tasks**:
- [ ] Implement hierarchical chunking (chapter → section → paragraph)
- [ ] Add semantic chunking based on content
- [ ] Implement chunk overlap strategy
- [ ] Add chunk metadata (source, page, position)

### Step 2.3: Embedding & Indexing
**File**: `app/services/embeddings.py`

**Tasks**:
- [ ] Generate embeddings using sentence-transformers
- [ ] Batch processing for large documents
- [ ] Store embeddings in Qdrant
- [ ] Link chunks to source documents

---

## Phase 3: API Development

### Step 3.1: Project Management Endpoints
**File**: `app/api/routes/projects.py`

**Endpoints**:
- [ ] `POST /projects/create` - Create new project
- [ ] `GET /projects/` - List user projects
- [ ] `GET /projects/{project_id}` - Get project details
- [ ] `DELETE /projects/{project_id}` - Delete project

### Step 3.2: File Upload Endpoints
**File**: `app/api/routes/documents.py`

**Endpoints**:
- [ ] `POST /projects/{project_id}/upload` - Upload files
- [ ] `GET /projects/{project_id}/documents` - List documents
- [ ] `DELETE /projects/{project_id}/documents/{doc_id}` - Remove document
- [ ] `GET /projects/{project_id}/documents/{doc_id}/status` - Processing status

### Step 3.3: Query Processing Endpoints
**File**: `app/api/routes/queries.py`

**Endpoints**:
- [ ] `POST /projects/{project_id}/query` - Submit query
- [ ] `GET /projects/{project_id}/history` - Get query history
- [ ] `GET /projects/{project_id}/queries/{query_id}` - Get specific query result

### Step 3.4: Google Drive Integration (Optional for later)
**File**: `app/api/routes/integrations.py`

**Endpoints**:
- [ ] `POST /projects/{project_id}/attach-google-drive` - Attach Drive files
- [ ] `GET /auth/google/callback` - OAuth callback

---

## Phase 4: RAG Query Pipeline

### Step 4.1: Query Processing Service
**File**: `app/services/query_processor.py`

**Tasks**:
- [ ] Query embedding generation
- [ ] Vector similarity search
- [ ] Context retrieval and ranking
- [ ] Re-ranking (optional)

### Step 4.2: LLM Integration Enhancement
**Files**: `app/services/llm_openai.py`, `app/services/llm_anthropic.py`

**Tasks**:
- [ ] Implement proper prompt engineering
- [ ] Add citation extraction
- [ ] Implement streaming responses (optional)
- [ ] Add error handling and retries

### Step 4.3: Response Generation with Citations
**File**: `app/services/response_generator.py`

**Tasks**:
- [ ] Format context for LLM
- [ ] Extract citations from context
- [ ] Calculate relevance scores
- [ ] Format final response with citations

---

## Phase 5: Data Persistence & Logging

### Step 5.1: Query History Storage
**File**: `app/services/storage.py` (enhance existing)

**Tasks**:
- [ ] Save queries to PostgreSQL
- [ ] Save responses with citations
- [ ] Implement conversation threading
- [ ] Add export functionality

### Step 5.2: Analytics & Metrics
**File**: `app/services/analytics.py`

**Tasks**:
- [ ] Track query performance
- [ ] Document usage statistics
- [ ] User activity metrics

---

## Phase 6: Testing & Quality Assurance

### Step 6.1: Unit Tests
**Directory**: `tests/`

**Tasks**:
- [ ] Test chunking algorithms
- [ ] Test embedding generation
- [ ] Test vector search
- [ ] Test API endpoints

### Step 6.2: Integration Tests
**Tasks**:
- [ ] End-to-end document upload → query flow
- [ ] Test with real PDFs
- [ ] Test concurrent requests

### Step 6.3: Playwright E2E Tests
**Tasks**:
- [ ] API endpoint testing via Swagger UI
- [ ] File upload automation
- [ ] Query submission testing

---

## Phase 7: Frontend Development (Future)

### Step 7.1: Frontend Setup
**Directory**: `frontend/`

**Tasks**:
- [ ] Initialize Next.js/React project
- [ ] Set up routing
- [ ] Configure API client

### Step 7.2: UI Components
**Tasks**:
- [ ] Project dashboard
- [ ] File upload interface
- [ ] Chat/query interface
- [ ] Document viewer
- [ ] Citations display

---

## Phase 8: Deployment & DevOps

### Step 8.1: Containerization
**Tasks**:
- [ ] Create Dockerfile
- [ ] Docker Compose setup (app + PostgreSQL + Qdrant)
- [ ] Environment configuration

### Step 8.2: Deployment
**Tasks**:
- [ ] Choose hosting platform (AWS, GCP, Azure, Railway, etc.)
- [ ] Set up CI/CD pipeline
- [ ] Configure production environment

---

## Immediate Next Steps (Starting Now)

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set up PostgreSQL database** (local or cloud)
3. **Set up Qdrant** (Docker or cloud)
4. **Create core configuration** (`app/core/config.py`)
5. **Define database models** (`app/models/`)
6. **Test database connection**
7. **Begin document processing pipeline**

---

## Development Priorities

### Must Have (MVP)
- ✅ Project structure
- ⏳ Core configuration
- ⏳ Database models
- ⏳ Document upload & processing
- ⏳ Basic chunking
- ⏳ Vector search
- ⏳ Query processing with OpenAI/Anthropic
- ⏳ Basic API endpoints

### Should Have
- Advanced chunking strategies
- Query history
- Analytics
- Better error handling
- API authentication

### Nice to Have
- Google Drive integration
- Frontend UI
- Real-time streaming
- Advanced re-ranking
- Multiple language support

---

## Estimated Timeline

- **Phase 1 (Core Infrastructure)**: 2-3 days
- **Phase 2 (Document Processing)**: 3-4 days
- **Phase 3 (API Development)**: 2-3 days
- **Phase 4 (RAG Pipeline)**: 2-3 days
- **Phase 5 (Persistence)**: 1-2 days
- **Phase 6 (Testing)**: 2-3 days
- **Phase 7 (Frontend)**: 5-7 days
- **Phase 8 (Deployment)**: 1-2 days

**Total MVP**: ~2-3 weeks
**Full Application**: ~4-6 weeks

---

*Last Updated: 2025-11-04*
