from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
from fastapi.middleware.cors import CORSMiddleware

from core.ingest import load_repo
from core.embedding import get_embeddings
from core.vector_store import VectorStore
from core.rag import rag_query
from utils.chunking import chunk_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = None
all_chunks = []
ready = False

def build_index(repo_url):
    global store, all_chunks, ready
    try:
        print(f"Building index for {repo_url}...")
        data = load_repo(repo_url)
        all_chunks = []
        for item in data:
            chunks = chunk_text(item["content"], chunk_size=500, overlap=100)
            for chunk in chunks:
                all_chunks.append({
                    "content": chunk,
                    "path": item["path"]
                })

        texts = [c["content"] for c in all_chunks]
        embeddings = get_embeddings(texts)

        store = VectorStore(len(embeddings[0]))
        store.add(embeddings, all_chunks)
        ready = True
        print("SERVER READY")
    except Exception as e:
        print("ERROR:", e)
        ready = False

class QueryRequest(BaseModel):
    query: str

class RepoRequest(BaseModel):
    repo_url: str

@app.post("/load_repo")
def load_new_repo(req: RepoRequest):
    global ready

    ready = False

    thread = Thread(target=build_index, args=(req.repo_url,), daemon=True)
    thread.start()

    return {"message": "Repository loading started..."}

@app.post("/query")
def query_codebase(req: QueryRequest):
    if not ready:
        return {"message": "Index building... please wait"}

    answer, results = rag_query(store, all_chunks, req.query)

    return {
        "answer": answer,
        "sources": [
            {
                "path": r["path"],
                "snippet": r["content"][:200] + "..."
            }
            for r in results
        ]
    }

@app.get("/")
def health():
    return {"status": "ready" if ready else "building"}