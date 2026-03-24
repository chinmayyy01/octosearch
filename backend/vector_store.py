import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.data = []
        
    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings).astype('float32'))
        self.data.extend(texts)
    
    def search(self, query_embedding, k=5):
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        
        results = [self.data[i] for i in indices[0]]
        return results