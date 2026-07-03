# OctoSearch

OctoSearch lets you ask questions about any GitHub repository in plain English. It fetches the code, builds a search index, and gives you answers with actual code snippets as references.

Live demo: https://octosearch-cm.vercel.app

The app uses a hybrid search approach combining vector embeddings and keyword matching to find the most relevant code, then uses an LLM to generate helpful responses.

## How it works

When you paste a GitHub repository URL, the app fetches all the code files directly from GitHub's API (no cloning needed). It then chunks the code into smaller pieces, creates embeddings for each chunk, and builds both a vector search index and a BM25 keyword index. When you ask a question, it searches both indexes to find the most relevant code snippets, and passes those to the LLM to generate a grounded answer.

## Tech stack

The backend is built with FastAPI and uses LangChain for the retrieval pipeline. It uses sentence-transformers for embeddings, FAISS for vector storage, and Groq's Llama model for generating answers. The frontend is a React app built with Vite and Tailwind CSS.

## Project structure

```
octosearch/
├── api.py                 Root entry point that loads the backend
├── modal_app.py           Modal deployment configuration
├── requirements.txt       Python dependencies
├── backend/
│   ├── api.py            FastAPI application and routes
│   ├── requirements.txt
│   ├── core/
│   │   ├── ingest.py     GitHub API file fetching
│   │   ├── embedding.py  Embedding generation with LangChain
│   │   ├── vector_store.py  FAISS vector store
│   │   ├── bm25.py       BM25 retriever
│   │   ├── rag.py        Hybrid retrieval and answer generation
│   │   └── llm.py        Groq LLM integration
│   └── utils/
│       ├── file_loader.py
│       └── chunking.py
└── frontend/
    ├── package.json
    ├── .env.example
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── services/
        │   └── octoApi.js
        └── components/
            ├── chat/
            ├── layout/
            └── load/
```

## Getting started locally

You need Python 3.10+, Node.js 18+, and a Groq API key.

First, set up the backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Then set up the frontend:

```bash
cd frontend
npm install
cd ..
```

Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Start the backend:

```bash
uvicorn api:app --reload
```

Start the frontend in another terminal:

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

## Deployment

The app is designed to run on Modal for the backend and Vercel for the frontend.

For Modal deployment, you need to set up secrets with your API keys:

```bash
modal secret create octosearch-secrets GROQ_API_KEY=your_groq_api_key
```

Optionally, add a GitHub token for higher API rate limits (60 requests/hour without token, 5000 with token):

```bash
modal secret update octosearch-secrets GITHUB_TOKEN=your_github_personal_access_token
```

Then deploy:

```bash
modal deploy modal_app.py
```

For the frontend, deploy to Vercel and set the `VITE_API_BASE_URL` environment variable to your Modal backend URL.

## API endpoints

POST `/load_repo` - Starts indexing a repository
Request: `{ "repo_url": "https://github.com/owner/repo" }`
Response: `{ "message": "Repository loading started..." }`

POST `/query` - Asks a question about the indexed code
Request: `{ "query": "How does authentication work?" }`
Response: `{ "answer": "...", "sources": [{ "path": "...", "snippet": "..." }] }`

GET `/` - Health check
Response: `{ "status": "building" }` or `{ "status": "ready" }`

## Common issues

If the frontend can't reach the backend, make sure `VITE_API_BASE_URL` is set correctly in your frontend environment. For CORS issues, the backend currently allows all origins. If queries fail, verify your Groq API key is set correctly.

## Screenshots

![OctoSearch Demo 1](./docs/Screenshot1.png)
![OctoSearch Demo 2](./docs/Screenshot2.png)