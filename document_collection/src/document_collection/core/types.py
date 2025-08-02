"""Type definitions for document collection."""

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeAlias, Union

# Type aliases for common types
PathLike: TypeAlias = Union[str, Path]
ConfigDict: TypeAlias = Dict[str, Any]
MetadataDict: TypeAlias = Dict[str, Any]
ErrorList: TypeAlias = List[str]
WarningList: TypeAlias = List[str]

# Callback type definitions
ProgressCallback: TypeAlias = Callable[[int, int, str], None]
CompletionCallback: TypeAlias = Callable[[bool, str], None]
ErrorCallback: TypeAlias = Callable[[Exception, str], None]

# Document processing related types
ConversionOptions: TypeAlias = Dict[str, Any]
RetrievalOptions: TypeAlias = Dict[str, Any]
ProcessingOptions: TypeAlias = Dict[str, Any]


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
MCPToolName: TypeAlias = str
MCPToolSchema: TypeAlias = Dict[str, Any]
MCPRequest: TypeAlias = Dict[str, Any]
MCPResponse: TypeAlias = Dict[str, Any]

# CLI related types
CLICommand: TypeAlias = str
CLIArguments: TypeAlias = Dict[str, Any]
CLIOptions: TypeAlias = Dict[str, Any]

# Configuration related types
ConfigurationSource: TypeAlias = Union[str, Path, Dict[str, Any]]

# File handling related types
FileExtension: TypeAlias = str
MimeType: TypeAlias = str
FileSize: TypeAlias = int  # Size in bytes
Checksum: TypeAlias = str  # SHA-256 hash

# Network related types
URL: TypeAlias = str
HTTPMethod: TypeAlias = str
HTTPHeaders: TypeAlias = Dict[str, str]
HTTPStatusCode: TypeAlias = int
TimeoutSeconds: TypeAlias = float

# Concurrency related types
WorkerCount: TypeAlias = int
QueueSize: TypeAlias = int
BatchSize: TypeAlias = int

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
