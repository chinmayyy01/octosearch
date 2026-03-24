from core.embedding import get_embeddings
from core.llm import generate_answer

def rag_query(store, query, k=3):
    query_embedding = get_embeddings([query])[0]
    results = store.search(query_embedding, k=k)
    
    context = "\n\n".join([f"File: {item['path']}\n{item['content']}" for item in results])
    
    answer = generate_answer(context, query)
    return answer, results