# cached_rag_pipeline.py
# cached_rag_pipeline.py

from typing import List
from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.caching.cache_checker import CacheChecker
from RAGPipeline import RAGPipelineServer

class CachedRAGPipeline:
    def __init__(self, hf_token: str):
        self.rag_pipeline = RAGPipelineServer(hf_token=hf_token)
        self.document_store = InMemoryDocumentStore()
        self.cache_checker = CacheChecker(self.document_store, cache_field="file_path")

    def add_document(self, file_path: str):
        # First, check if the document is already in the cache
        results = self.cache_checker.run(items=[file_path])
        if results["hits"]:
            print(f"Document '{file_path}' is already in the cache.")
            return

        # If not in cache, add to RAG pipeline and cache
        self.rag_pipeline.add_document(file_path)
        document = Document(content="", meta={"file_path": file_path})
        self.document_store.write_documents([document])
        print(f"Document '{file_path}' has been added to the RAG pipeline and cache.")

    def run_pipeline(self, question: str) -> str:
        return self.rag_pipeline.run_pipeline(question)

    def clear_cache(self):
        self.document_store.delete_documents()
        print("Cache has been cleared.")

    def list_cached_documents(self) -> List[str]:
        # Use filter_documents with no filters to get all documents
        all_docs = self.document_store.filter_documents()
        return [doc.meta["file_path"] for doc in all_docs]