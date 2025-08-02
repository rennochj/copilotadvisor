"""Custom exceptions for document collection."""

from typing import Any


class DocumentCollectionError(Exception):
    """Base exception for document collection operations."""

    def __init__(
        self,
        message: str,
        source: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize exception.

        Args:
            message: Error message
            source: Source that caused the error
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.source = source
        self.details = details or {}


class RetrievalError(DocumentCollectionError):
    """Exception raised when document retrieval fails."""

    def __init__(
        self,
        message: str,
        source: str | None = None,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize retrieval error.

        Args:
            message: Error message
            source: Source that failed to retrieve
            status_code: HTTP status code (for web retrievals)
            details: Additional error details
        """
        super().__init__(message, source, details)
        self.status_code = status_code


class ConversionError(DocumentCollectionError):
    """Exception raised when document conversion fails."""

    def __init__(
        self,
        message: str,
        source: str | None = None,
        input_format: str | None = None,
        output_format: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize conversion error.

        Args:
            message: Error message
            source: Source document that failed to convert
            input_format: Input document format
            output_format: Target output format
            details: Additional error details
        """
        super().__init__(message, source, details)
        self.input_format = input_format
        self.output_format = output_format


class ValidationError(DocumentCollectionError):
    """Exception raised when input validation fails."""

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: Any | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize validation error.

        Args:
            message: Error message
            field: Field that failed validation
            value: Value that failed validation
            details: Additional error details
        """
        super().__init__(message, details=details)
        self.field = field
        self.value = value


class ConfigurationError(DocumentCollectionError):
    """Exception raised when configuration is invalid."""

    def __init__(
        self,
        message: str,
        config_key: str | None = None,
        config_value: Any | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize configuration error.

        Args:
            message: Error message
            config_key: Configuration key that caused the error
            config_value: Configuration value that caused the error
            details: Additional error details
        """
        super().__init__(message, details=details)
        self.config_key = config_key
        self.config_value = config_value


class UnsupportedFormatError(DocumentCollectionError):
    """Exception raised when document format is not supported."""

    def __init__(
        self,
        message: str,
        format: str | None = None,
        supported_formats: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize unsupported format error.

        Args:
            message: Error message
            format: Unsupported format
            supported_formats: List of supported formats
            details: Additional error details
        """
        super().__init__(message, details=details)
        self.format = format
        self.supported_formats = supported_formats or []


class NetworkError(RetrievalError):
    """Exception raised when network operations fail."""

    def __init__(
        self,
        message: str,
        source: str | None = None,
        status_code: int | None = None,
        timeout: bool | None = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize network error.

        Args:
            message: Error message
            source: URL that caused the error
            status_code: HTTP status code
            timeout: Whether error was due to timeout
            details: Additional error details
        """
        super().__init__(message, source, status_code, details)
        self.timeout = timeout


class FileSystemError(RetrievalError):
    """Exception raised when file system operations fail."""

    def __init__(
        self,
        message: str,
        source: str | None = None,
        permission_denied: bool | None = False,
        not_found: bool | None = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize file system error.

        Args:
            message: Error message
            source: File path that caused the error
            permission_denied: Whether error was due to permission denied
            not_found: Whether error was due to file not found
            details: Additional error details
        """
        super().__init__(message, source, details=details)
        self.permission_denied = permission_denied
        self.not_found = not_found


class ProcessingError(DocumentCollectionError):
    """Exception raised when document processing fails."""

    def __init__(
        self,
        message: str,
        source: str | None = None,
        stage: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize processing error.

        Args:
            message: Error message
            source: Source that was being processed
            stage: Processing stage where error occurred
            details: Additional error details
        """
        super().__init__(message, source, details)
        self.stage = stage


# Exception mapping for common error types
ERROR_MAPPING = {
    "file_not_found": FileSystemError,
    "permission_denied": FileSystemError,
    "network_timeout": NetworkError,
    "invalid_url": ValidationError,
    "unsupported_format": UnsupportedFormatError,
    "conversion_failed": ConversionError,
    "retrieval_failed": RetrievalError,
    "processing_failed": ProcessingError,
    "config_invalid": ConfigurationError,
}
