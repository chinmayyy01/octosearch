from ingest import load_repo
from utils.chunking import chunk_text
from embedding import get_embeddings
from vector_store import VectorStore

#Step 1: Load repo
repo_url = "https://github.com/psf/requests"
data = load_repo(repo_url)

#Step 2: Create chunks with metadata
all_chunks = []

for item in data:
    chunks = chunk_text(item["content"], chunk_size=500, overlap=100)
    
    for chunk in chunks:
        all_chunks.append({
            "content": chunk,
            "path": item["path"]
        })

print(f"Total chunks created: {len(all_chunks)}")

#Step 3: Extract only text for embeddings
texts = [item["content"] for item in all_chunks]

#Step 4: Generate embeddings
embeddings = get_embeddings(texts)

#Step 5: Build vector store
store = VectorStore(len(embeddings[0]))
store.add(embeddings, all_chunks)

print("Index built successfully.\n")

# Step 6: Query
query = "how is authentication implemented"

query_embedding = get_embeddings([query])[0]

results = store.search(query_embedding, k=3)

#Step 7: Display results
print("Top results:\n")

for i, r in enumerate(results):
    print(f"Result {i+1}")
    print(f"File: {r['path']}")
    print(f"Code:\n{r['content'][:300]}")
    print("-" * 50)