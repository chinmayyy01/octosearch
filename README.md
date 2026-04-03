````markdown
# OctoSearch

OctoSearch is a codebase understanding system that allows users to query any GitHub repository using natural language. It uses a retrieval augmented generation (RAG) pipeline to analyze source code and generate structured explanations with source references.

---

## Features

- Dynamic repository ingestion using GitHub URLs  
- Hybrid retrieval using semantic embeddings and keyword search  
- Structured answers with clear explanations of code components  
- Source attribution with file paths and code snippets  
- Full stack system with React frontend and FastAPI backend  

---

## Architecture

### Frontend
- React  
- TailwindCSS  

### Backend
- FastAPI  

### Core System
- Repository ingestion and parsing  
- Text chunking with overlap  
- Embedding generation using sentence transformers  
- Vector search using FAISS  
- Keyword search using BM25  
- Hybrid retrieval combining semantic and keyword search  
- Large language model for answer generation  

---

## Folder Structure

```text
octosearch/
│
├── backend/
│   ├── api.py
│   ├── core/
│   │   ├── ingest.py
│   │   ├── embedding.py
│   │   ├── vector_store.py
│   │   ├── rag.py
│   │   ├── bm25.py
│   │   └── llm.py
│   │
│   ├── utils/
│   │   ├── file_loader.py
│   │   └── chunking.py
│   │
│   ├── scripts/
│   │   ├── test_rag.py
│   │   └── build_index.py
│   │
│   ├── data/
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── index.html
│   ├── package.json
│   └── tailwind.config.js
│
├── .gitignore
└── README.md
````

---

## Workflow

1. User provides a GitHub repository URL
2. Backend clones and processes the repository
3. Code is split into chunks and embedded
4. A vector index is created for retrieval
5. User asks a question
6. System retrieves relevant chunks using hybrid search
7. LLM generates a structured answer based on retrieved context

---

## API Endpoints

### POST /load_repo

Loads and indexes a repository

### POST /query

Returns an answer along with source snippets

### GET /

Returns system status

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/octosearch.git
cd octosearch
```

---

## Setup

### Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

---

## Running the Project

### Start Backend

```bash
cd backend
uvicorn api:app --reload
```

### Start Frontend

```bash
cd frontend
npm run dev
```

### Open in Browser

```text
http://localhost:5173
```

---

## Usage

* Enter a GitHub repository URL and load it
* Wait for indexing to complete
* Ask questions about the codebase
* View structured answers and source references

---

## Limitations

* Indexing is performed per repository and may take time
* Performance depends on repository size
* Answers are limited to retrieved context

---

## Future Improvements

* Caching indexed repositories
* Improved ranking strategies
* Enhanced UI and interaction
* VS Code extension integration

```
```
