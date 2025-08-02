"""Web HTTP retriever implementation for document collection."""

from pathlib import Path
from typing import Any

import requests

from document_collection.core.interfaces import DocumentRetriever


class WebHttpRetriever(DocumentRetriever):
    """Retrieve documents from web HTTP/HTTPS sources."""

    def can_handle(self, source: str) -> bool:
        return source.lower().startswith(("http://", "https://"))

    def get_metadata(self, source: str) -> None:
        # For web sources, metadata is limited before download
        return None

    async def retrieve(
        self, source: str, destination: Path, request_id: str = "", **kwargs: Any
    ) -> Path:
        # Validate URL
        if not source.lower().startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL: {source}")
        try:
            response = requests.get(
                source, stream=True, timeout=kwargs.get("timeout", 10)
            )
            response.raise_for_status()
            filename = kwargs.get("filename") or source.split("/")[-1]
            dest_path = destination / filename
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return dest_path
        except Exception as e:
            raise RuntimeError(f"Error retrieving web document: {e}") from e
