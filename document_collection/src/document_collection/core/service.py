"""Document collection service - main orchestration logic."""

import logging
import time
from pathlib import Path
from typing import Any

from ..converters.factory import ConverterFactory
from ..retrievers.factory import RetrieverFactory
from .config import get_config
from .exceptions import ValidationError
from .models import (
    CollectionRequest,
    CollectionResult,
    DocumentFormat,
    DocumentMetadata,
    DocumentSource,
    SourceType,
)

logger = logging.getLogger(__name__)


class DocumentCollectionService:
    """Main service for document collection operations."""

    def __init__(self) -> None:
        """Initialize the document collection service."""
        logger.debug("Initializing DocumentCollectionService")
        self.config = get_config()
        self.retriever_factory = RetrieverFactory()
        self.converter_factory = ConverterFactory()
        logger.debug(
            "DocumentCollectionService initialized with config: %s", self.config
        )

    async def collect_document(
        self, source: str, destination_path: Path | None = None, **options: Any
    ) -> CollectionResult:
        """Collect a single document.

        Args:
            source: Source file path or URL
            destination_path: Destination directory
            **options: Additional processing options

        Returns:
            Collection result

        Raises:
            DocumentCollectionError: If collection fails

        """
        start_time = time.time()
        logger.debug("Collecting document from source: %s", source)
        logger.debug("Options: %s", options)

        try:
            # Validate inputs
            if not source:
                raise ValidationError("Source cannot be empty")

            # Use default destination if not provided
            if destination_path is None:
                destination_path = self.config.destination_path

            # Ensure destination directory exists
            destination_path.mkdir(parents=True, exist_ok=True)

            # Create collection request
            request = CollectionRequest(
                source=source, destination_path=destination_path, **options
            )

            # Get appropriate retriever
            retriever = self.retriever_factory.get_retriever(source)

            # Retrieve document
            retrieved_path = await retriever.retrieve(
                source=source,
                destination=destination_path,
                request_id=str(hash(source)),
                **options,
            )

            # Get metadata
            metadata = retriever.get_metadata(source)
            if metadata is None:
                # Create basic metadata if retriever doesn't provide it
                filename = Path(source).name
                # Try to determine format from file extension
                extension = Path(source).suffix.lower().lstrip(".")
                try:
                    doc_format = DocumentFormat(extension)
                except ValueError:
                    # Default to PDF if format cannot be determined
                    doc_format = DocumentFormat.PDF

                metadata = DocumentMetadata(
                    filename=filename,
                    source=DocumentSource(
                        source=source,
                        source_type=SourceType.LOCAL_FILE
                        if not source.startswith(("http://", "https://"))
                        else SourceType.WEB_URL,
                    ),
                    format=doc_format,
                    size_bytes=None,
                    created_at=None,
                    modified_at=None,
                    checksum=None,
                )

            # Convert to markdown if requested and supported
            output_path = retrieved_path
            if request.convert_to_markdown:
                try:
                    converter = self.converter_factory.get_converter(source)
                    # Generate output filename with .md extension
                    output_filename = Path(retrieved_path.stem + ".md")
                    markdown_path = destination_path / output_filename

                    output_path = await converter.convert(
                        input_path=retrieved_path, output_path=markdown_path, **options
                    )
                except ValueError:
                    # Converter not available for this file type
                    # Keep original file
                    pass

            processing_time = time.time() - start_time
            logger.debug("Document collection completed in %s seconds", processing_time)

            return CollectionResult(
                success=True,
                source=source,
                output_path=output_path,
                original_path=retrieved_path if output_path != retrieved_path else None,
                metadata=metadata,
                processing_time_seconds=processing_time,
                errors=[],
                warnings=[],
            )

        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            logger.error("Error collecting document: %s", error_msg)

            return CollectionResult(
                success=False,
                source=source,
                output_path=None,
                original_path=None,
                metadata=None,
                processing_time_seconds=processing_time,
                errors=[error_msg],
                warnings=[],
            )

    async def collect_documents(
        self, sources: list[str], destination_path: Path | None = None, **options: Any
    ) -> list[CollectionResult]:
        """Collect multiple documents.

        Args:
            sources: List of source file paths or URLs
            destination_path: Destination directory
            **options: Additional processing options

        Returns:
            List of collection results

        """
        results = []
        for source in sources:
            result = await self.collect_document(source, destination_path, **options)
            results.append(result)
        return results
