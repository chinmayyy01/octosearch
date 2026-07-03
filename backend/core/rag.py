from backend.core.llm import generate_answer
from backend.core.bm25 import BM25Retriever

def rag_query(store, all_chunks, query, k=5):
    vector_results = store.search(query, k=k)

    texts = [c["content"] for c in all_chunks]
    metadatas = [{"path": c["path"]} for c in all_chunks]
    bm25 = BM25Retriever(texts, metadatas)
    bm25_results = bm25.search(query, k=k)

    combined = vector_results + bm25_results

    seen = set()
    unique_results = []
    for r in combined:
        key = r["content"]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    context = "\n\n".join([
        f"File: {r['path']}\n{r['content']}"
        for r in unique_results[:k]
    ])

    answer = generate_answer(context, query)

    return answer, unique_results[:k]