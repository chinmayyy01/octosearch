from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class VectorStore:
    def __init__(self):
        self.index = None
        self.documents = []

    def add(self, texts, metadatas):
        documents = [Document(page_content=text, metadata=metadata) for text, metadata in zip(texts, metadatas)]
        self.documents.extend(documents)
        if self.index is None:
            from backend.core.embedding import get_embeddings
            embeddings = get_embeddings()
            self.index = FAISS.from_documents(documents, embeddings)
        else:
            from backend.core.embedding import get_embeddings
            embeddings = get_embeddings()
            self.index.add_documents(documents, embeddings)

    def search(self, query, k=5):
        results = self.index.similarity_search(query, k=k)
        return [{"content": doc.page_content, "path": doc.metadata.get("path", "")} for doc in results]