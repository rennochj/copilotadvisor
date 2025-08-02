"""Type definitions for document collection."""

from collections.abc import Callable
from enum import Enum
from pathlib import Path
from typing import Any

# Type aliases for common types
type PathLike = str | Path
type ConfigDict = dict[str, Any]
type MetadataDict = dict[str, Any]
type ErrorList = list[str]
type WarningList = list[str]

# Callback type definitions
type ProgressCallback = Callable[[int, int, str], None]
type CompletionCallback = Callable[[bool, str], None]
type ErrorCallback = Callable[[Exception, str], None]

# Document processing related types
type ConversionOptions = dict[str, Any]
type RetrievalOptions = dict[str, Any]
type ProcessingOptions = dict[str, Any]


class LogLevel(str, Enum):
    """Logging levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ProcessingStage(str, Enum):
    """Document processing stages."""

    VALIDATION = "validation"
    RETRIEVAL = "retrieval"
    CONVERSION = "conversion"
    STORAGE = "storage"
    CLEANUP = "cleanup"
    COMPLETED = "completed"


class RetryStrategy(str, Enum):
    """Retry strategies for failed operations."""

    NONE = "none"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    CUSTOM = "custom"


class OutputFormat(str, Enum):
    """Output format options."""

    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    XML = "xml"


class CompressionType(str, Enum):
    """Compression types for archived documents."""

    NONE = "none"
    GZIP = "gzip"
    ZIP = "zip"
    TAR = "tar"
    TAR_GZ = "tar.gz"


class AuthenticationType(str, Enum):
    """Authentication types for web retrieval."""

    NONE = "none"
    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH = "oauth"


class ValidationLevel(str, Enum):
    """Validation levels for input checking."""

    NONE = "none"
    BASIC = "basic"
    STRICT = "strict"
    PARANOID = "paranoid"


# MCP (Model Context Protocol) related types
type MCPToolName = str
type MCPToolSchema = dict[str, Any]
type MCPRequest = dict[str, Any]
type MCPResponse = dict[str, Any]

# CLI related types
type CLICommand = str
type CLIArguments = dict[str, Any]
type CLIOptions = dict[str, Any]

# Configuration related types
type ConfigurationSource = str | Path | dict[str, Any]

# File handling related types
type FileExtension = str
type MimeType = str
type FileSize = int  # Size in bytes
type Checksum = str  # SHA-256 hash

# Network related types
type URL = str
type HTTPMethod = str
type HTTPHeaders = dict[str, str]
type HTTPStatusCode = int
type TimeoutSeconds = float

# Concurrency related types
type WorkerCount = int
type QueueSize = int
type BatchSize = int

# Constants
DEFAULT_DESTINATION = Path("./documents")
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_WORKERS = 4
DEFAULT_BATCH_SIZE = 10
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 1.0

# File size limits (in bytes)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_BATCH_SIZE = 1000  # Maximum files in batch
MAX_CONCURRENT_DOWNLOADS = 10

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "md": "text/markdown",
    "txt": "text/plain",
}

# HTTP related constants
USER_AGENT = "DocumentCollection/0.1.0"
ACCEPTED_CONTENT_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/markdown",
    "text/plain",
]
