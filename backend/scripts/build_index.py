from backend.core.ingest import load_repo
from utils.chunking import chunk_text
from backend.core.embedding import get_embeddings
from backend.core.vector_store import VectorStore

repo_url = "https://github.com/psf/requests"

data = load_repo(repo_url)

all_chunks = []

for item in data:
    chunks = chunk_text(item['content'])
    for chunk in chunks:
        all_chunks.append([{
            "content" : chunk,
            "path": item["path"]
        }])

texts = [item["content"] for item in all_chunks]
embeddings = get_embeddings(texts)

store = VectorStore(len(embeddings[0]))
store.add(embeddings, all_chunks)

print("Index built with", len(all_chunks), "chunks.")