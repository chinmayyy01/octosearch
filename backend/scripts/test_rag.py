from core.ingest import load_repo
from core.embedding import get_embeddings
from core.vector_store import VectorStore
from core.rag import rag_query
from utils.chunking import chunk_text

repo_url = "https://github.com/psf/requests"

data = load_repo(repo_url)

all_chunks = []

for item in data:
    chunks = chunk_text(item["content"], chunk_size=500, overlap=100)
    
    for chunk in chunks:
        all_chunks.append({
            "content": chunk,
            "path": item["path"]
        })

print(f"Total chunks: {len(all_chunks)}")

texts = [c["content"] for c in all_chunks]
embeddings = get_embeddings(texts)

store = VectorStore(len(embeddings[0]))
store.add(embeddings, all_chunks)

print("Index ready.\n")

query = "How is authentication implemented?"

answer, results = rag_query(store, all_chunks, query)

print("=== ANSWER ===\n")
print(answer)

print("\n=== SOURCES ===\n")
for r in results:
    print(r["path"])