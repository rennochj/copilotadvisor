"""PowerPoint to Markdown converter implementation."""

from pathlib import Path
from typing import Any

from document_collection.core.interfaces import DocumentConverter


class PowerPointConverter(DocumentConverter):
    """Convert PowerPoint documents to Markdown format."""

    def can_convert(self, file_path: Path) -> bool:
        return str(file_path).lower().endswith(".pptx")

    def get_supported_formats(self) -> list[str]:
        return ["pptx"]

    async def convert(self, input_path: Path, output_path: Path, **kwargs: Any) -> Path:
        # TODO: Implement PowerPoint parsing and conversion logic
        # Placeholder: just return output_path
        return output_path
