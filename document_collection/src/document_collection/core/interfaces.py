"""Abstract interfaces for document collection components."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from .models import CollectionResult, DocumentMetadata


class DocumentRetriever(ABC):
    """Abstract base class for document retrievers."""

    @abstractmethod
    async def retrieve(self, source: str, destination: Path, **kwargs: Any) -> Path:
        """
        Retrieve a document from the specified source.

        Args:
            source: Source location (file path or URL)
            destination: Destination directory
            **kwargs: Additional retriever-specific options

        Returns:
            Path to the retrieved document

        Raises:
            RetrievalError: If document cannot be retrieved
        """
        pass

    @abstractmethod
    def can_handle(self, source: str) -> bool:
        """
        Check if this retriever can handle the given source.

        Args:
            source: Source location to check

        Returns:
            True if this retriever can handle the source
        """
        pass

    @abstractmethod
    def get_metadata(self, source: str) -> DocumentMetadata | None:
        """
        Get metadata for a document without retrieving it.

        Args:
            source: Source location

        Returns:
            Document metadata if available, None otherwise
        """
        pass


class DocumentConverter(ABC):
    """Abstract base class for document converters."""

    @abstractmethod
    async def convert(self, input_path: Path, output_path: Path, **kwargs: Any) -> Path:
        """
        Convert a document to markdown format.

        Args:
            input_path: Path to input document
            output_path: Path for output markdown file
            **kwargs: Additional converter-specific options

        Returns:
            Path to the converted document

        Raises:
            ConversionError: If document cannot be converted
        """
        pass

    @abstractmethod
    def can_convert(self, file_path: Path) -> bool:
        """
        Check if this converter can handle the given file type.

        Args:
            file_path: Path to file to check

        Returns:
            True if this converter can handle the file
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported file formats.

        Returns:
            List of supported file extensions (without dots)
        """
        pass


class DocumentProcessor(ABC):
    """Abstract base class for document processors."""

    @abstractmethod
    async def process(
        self,
        source: str,
        destination: Path,
        convert_to_markdown: bool = True,
        preserve_original: bool = False,
        **kwargs: Any,
    ) -> CollectionResult:
        """
        Process a document (retrieve and optionally convert).

        Args:
            source: Source location (file path or URL)
            destination: Destination directory
            convert_to_markdown: Whether to convert to markdown
            preserve_original: Whether to keep original file
            **kwargs: Additional processing options

        Returns:
            Collection result with processing details
        """
        pass


class ConfigurationProvider(ABC):
    """Abstract base class for configuration providers."""

    @abstractmethod
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        pass

    @abstractmethod
    def set_config(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        pass

    @abstractmethod
    def get_all_config(self) -> dict[str, Any]:
        """
        Get all configuration values.

        Returns:
            Dictionary of all configuration values
        """
        pass


class ProgressReporter(ABC):
    """Abstract base class for progress reporting."""

    @abstractmethod
    def report_progress(
        self, current: int, total: int, message: str = "", **metadata: Any
    ) -> None:
        """
        Report processing progress.

        Args:
            current: Current progress value
            total: Total progress value
            message: Progress message
            **metadata: Additional metadata
        """
        pass

    @abstractmethod
    def report_completion(self, success: bool, message: str = "") -> None:
        """
        Report processing completion.

        Args:
            success: Whether processing was successful
            message: Completion message
        """
        pass

    @abstractmethod
    def report_error(self, error: Exception, message: str = "") -> None:
        """
        Report processing error.

        Args:
            error: Exception that occurred
            message: Error message
        """
        pass
