"""DocumentRetrievalManager for batch and concurrent retrievals."""

from pathlib import Path

from document_collection.retrievers.factory import RetrieverFactory


class DocumentRetrievalManager:
    """Manages document retrieval operations."""

    def __init__(self) -> None:
        """Initialize the retriever manager."""
        self.factory = RetrieverFactory()

    async def retrieve_batch(self, sources: list[str], destination: Path) -> list[Path]:
        """Retrieve multiple documents in batch."""
        results = []
        for source in sources:
            retriever = self.factory.get_retriever(source)
            result = await retriever.retrieve(source, destination)
            results.append(result)
        return results
