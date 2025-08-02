"""Retriever factory for document collection."""

from document_collection.core.interfaces import DocumentRetriever
from document_collection.retrievers.local_retriever import LocalFileRetriever
from document_collection.retrievers.web_retriever import WebHttpRetriever


class RetrieverFactory:
    """Factory to instantiate appropriate retriever based on source type."""

    @staticmethod
    def get_retriever(source: str) -> DocumentRetriever:
        if source.lower().startswith(("http://", "https://")):
            return WebHttpRetriever()
        return LocalFileRetriever()
