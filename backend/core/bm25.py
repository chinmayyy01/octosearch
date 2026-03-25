from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self, texts):
        self.texts = texts
        self.tokenized = [text.split() for text in texts]
        self.bm25 = BM25Okapi(self.tokenized)

    def search(self, query, k=5):
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)        
        top_k = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return top_k