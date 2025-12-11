# RAG Web Application

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) web application designed to enable users to create projects by uploading PDFs or attaching files from Google Drive. The system uses a hierarchical chunking approach to segment documents for efficient semantic search and retrieval, capable of handling any number of files.

The application supports advanced quantitative data retrieval and analytics, integrates OpenAI or Anthropic large language models (LLMs) for query processing, and returns outputs with citations and relevance scores. Every user query and system response is saved into a continuous master file associated with each project, ensuring full conversation retention for auditing and further analysis.

## Key Features

- Project-based user workspace for document upload and Google Drive attachment
- Hierarchical chunking of documents for fine-grained retrieval
- Scalable implementation supporting any number of files
- Quantitative data parsing and advanced analytics capabilities
- Query processing using OpenAI or Anthropic APIs with citation and scoring
- Continuous logging of all query outputs and chat history per project

## Technology Stack

- **Backend**: Python FastAPI (with routes for upload, project management, query handling)
- **Frontend**: React or Next.js for project UI and conversation interface
- **Storage**: PostgreSQL for projects, queries, logs; Qdrant for vector search
- **LLM APIs**: OpenAI GPT models or Anthropic Claude models
- **Data Processing**: Hierarchical chunking, text and table extraction for retrieval and analytics

## Project Structure

```
Rag_App/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── routes/             # API route handlers
│   ├── core/                   # Core configuration and settings
│   ├── models/                 # Database models and schemas
│   ├── services/               # Business logic services
│   │   ├── __init__.py
│   │   ├── chunking.py         # Hierarchical chunking implementation
│   │   ├── llm_openai.py       # OpenAI integration
│   │   ├── llm_anthropic.py    # Anthropic integration
│   │   └── storage.py          # Query/output storage service
│   └── utils/                  # Utility functions
├── data/
│   ├── uploads/                # Uploaded files storage
│   └── processed/              # Processed data and query logs
├── tests/                      # Unit and integration tests
├── frontend/                   # Frontend application (React/Next.js)
├── docs/                       # Additional documentation
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://your-repo-url.git
cd Rag_App
```

### 2. Create and activate Python virtual environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Install required Python packages

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the `.env.example` file to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys and configuration:
- `OPENAI_API_KEY` - Your OpenAI API key
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `DATABASE_URL` - Your PostgreSQL connection string
- `QDRANT_HOST` - Qdrant vector database host
- Other configuration as needed

### 5. Set up the database

```bash
# Create PostgreSQL database
# Run migrations (to be implemented)
```

### 6. Run the backend server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

### 7. Start the frontend app (optional)

```bash
cd frontend
npm install
npm start
```

## Usage

1. **Create a new project** via the frontend or API endpoint `/projects/create`
2. **Upload PDFs** or attach Google Drive files to the project
3. The system ingests and chunks documents hierarchically for search
4. **Query** the project knowledge base via natural language questions
5. View results with **citations** and **relevance scores**
6. All queries and responses are saved continuously for reference

## API Endpoints

- `POST /projects/create` - Create a new project
- `POST /projects/{project_id}/upload` - Upload files to a project
- `POST /projects/{project_id}/attach-google-drive` - Attach Google Drive files
- `POST /projects/{project_id}/query` - Query the project knowledge base
- `GET /projects/{project_id}/history` - Get query history

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black app/
flake8 app/
```

## Next Steps

1. Implement database models and migrations
2. Create API route handlers in `app/api/routes/`
3. Implement vector database integration
4. Build document processing pipeline
5. Create frontend UI
6. Add authentication and authorization
7. Implement comprehensive testing

## Contributing

Contributions are welcome. Please open issues or pull requests for enhancements and bugfixes.

## License

Specify your license here.
