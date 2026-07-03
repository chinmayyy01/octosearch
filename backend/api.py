from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread, Lock
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.core.ingest import load_repo
from backend.core.vector_store import VectorStore
from backend.core.rag import rag_query
from backend.utils.chunking import chunk_text

app = FastAPI()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
cors_origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = None
all_chunks = []
ready = False
index_lock = Lock()

def build_index(repo_url):
    global store, all_chunks, ready
    with index_lock:
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

            if not all_chunks:
                print("ERROR: No chunks found in repository")
                ready = False
                return

            texts = [c["content"] for c in all_chunks]
            metadatas = [{"path": c["path"]} for c in all_chunks]

            store = VectorStore()
            store.add(texts, metadatas)
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
    try:
        with index_lock:
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
    except Exception as e:
        print(f"Query error: {e}")
        return {"message": f"Error processing query: {str(e)}"}

@app.get("/")
def health():
    return {"status": "ready" if ready else "building"}