"""Local file retriever implementation for document collection."""

from pathlib import Path
from typing import Any

from document_collection.core.interfaces import DocumentRetriever
from document_collection.core.models import (
    DocumentFormat,
    DocumentMetadata,
    DocumentSource,
    SourceType,
)


class LocalFileRetriever(DocumentRetriever):
    """Retrieve documents from the local filesystem."""

    def can_handle(self, source: str) -> bool:
        return not source.lower().startswith(("http://", "https://"))

    def get_metadata(self, source: str) -> DocumentMetadata | None:
        path = Path(source)
        if not path.exists() or not path.is_file():
            return None
        stat = path.stat()
        return DocumentMetadata(
            filename=path.name,
            source=DocumentSource(source=source, source_type=SourceType.LOCAL_FILE),
            format=DocumentFormat(path.suffix.lstrip(".").lower())
            if path.suffix
            else DocumentFormat.MARKDOWN,
            size_bytes=stat.st_size,
            created_at=None,
            modified_at=None,
            checksum=None,
        )

    async def retrieve(
        self, source: str, destination: Path, request_id: str = "", **kwargs: Any
    ) -> Path:
        source_path = Path(source)
        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {source_path}")
        if not source_path.is_file():
            raise ValueError(f"Source is not a file: {source_path}")
        try:
            import shutil

            # Ensure destination directory exists
            destination.mkdir(parents=True, exist_ok=True)

            # Copy file to destination directory
            dest_file = destination / source_path.name
            shutil.copy2(source_path, dest_file)

            return dest_file
        except Exception as e:
            raise RuntimeError(f"Error retrieving file: {e}") from e
