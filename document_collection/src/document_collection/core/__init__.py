"""Core module for document collection."""

from .config import Configuration, get_config, reset_config, set_config
from .exceptions import (
    ConfigurationError,
    ConversionError,
    DocumentCollectionError,
    FileSystemError,
    NetworkError,
    ProcessingError,
    RetrievalError,
    UnsupportedFormatError,
    ValidationError,
)
from .interfaces import (
    ConfigurationProvider,
    DocumentConverter,
    DocumentProcessor,
    DocumentRetriever,
    ProgressReporter,
)
from .models import (
    BatchCollectionRequest,
    BatchCollectionResult,
    CollectionRequest,
    CollectionResult,
    DocumentFormat,
    DocumentMetadata,
    DocumentSource,
    SourceType,
)
from .types import (
    AuthenticationType,
    CompressionType,
    LogLevel,
    OutputFormat,
    ProcessingStage,
    RetryStrategy,
    ValidationLevel,
)

__all__ = [
    # Configuration
    "Configuration",
    "get_config",
    "set_config", 
    "reset_config",
    
    # Models
    "DocumentFormat",
    "DocumentMetadata",
    "DocumentSource",
    "SourceType",
    "CollectionRequest",
    "CollectionResult",
    "BatchCollectionRequest",
    "BatchCollectionResult",
    
    # Interfaces
    "DocumentRetriever",
    "DocumentConverter", 
    "DocumentProcessor",
    "ConfigurationProvider",
    "ProgressReporter",
    
    # Exceptions
    "DocumentCollectionError",
    "RetrievalError",
    "ConversionError",
    "ValidationError",
    "ConfigurationError",
    "UnsupportedFormatError",
    "NetworkError",
    "FileSystemError",
    "ProcessingError",
    
    # Types and Enums
    "LogLevel",
    "ProcessingStage",
    "RetryStrategy",
    "OutputFormat",
    "CompressionType",
    "AuthenticationType",
    "ValidationLevel",
]
