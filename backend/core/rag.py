from core.embedding import get_embeddings
from core.llm import generate_answer
from core.bm25 import BM25Retriever


def rag_query(store, all_chunks, query, k=5):
    query_embedding = get_embeddings([query])[0]
    vector_results = store.search(query_embedding, k=k)

    texts = [c["content"] for c in all_chunks]
    bm25 = BM25Retriever(texts)
    bm25_indices = bm25.search(query, k=k)

    bm25_results = [all_chunks[i] for i in bm25_indices]

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