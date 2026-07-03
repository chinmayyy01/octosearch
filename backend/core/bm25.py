from langchain_community.retrievers import BM25Retriever as LangChainBM25Retriever
from langchain_core.documents import Document

class BM25Retriever:
    def __init__(self, texts, metadatas):
        documents = [Document(page_content=text, metadata=metadata) for text, metadata in zip(texts, metadatas)]
        self.retriever = LangChainBM25Retriever.from_documents(documents)

    def search(self, query, k=5):
        results = self.retriever.get_relevant_documents(query, k=k)
        return [{"content": doc.page_content, "path": doc.metadata.get("path", "")} for doc in results]