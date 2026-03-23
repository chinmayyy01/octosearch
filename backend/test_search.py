from ingest import load_repo
from utils.chunking import chunk_text
from embedding import get_embeddings
from vector_store import VectorStore

repo_url = "https://github.com/psf/requests"

data = load_repo(repo_url)

all_chunks = []

for item in data:
    chunks = chunk_text(item['content'])
    all_chunks.extend(chunks)

embeddings = get_embeddings(all_chunks)

store = VectorStore(len(embeddings[0]))
store.add(embeddings, all_chunks)

print("Index built with", len(all_chunks), "chunks.\n")

query = "authentication login request"

query_emb = get_embeddings([query])[0]

results = store.search(query_emb, k=3)

print("Top results:\n")

for i, r in enumerate(results):
    print(f"Result {i+1}:\n{r[:300]}")
    print("-" * 50)