"""Core data models for document collection."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator


class DocumentFormat(str, Enum):
    """Supported document formats."""
    
    PDF = "pdf"
    WORD = "docx"
    POWERPOINT = "pptx"
    EXCEL = "xlsx"
    MARKDOWN = "md"


class SourceType(str, Enum):
    """Document source types."""
    
    LOCAL_FILE = "local_file"
    WEB_URL = "web_url"


class DocumentSource(BaseModel):
    """Document source information."""
    
    source: str = Field(..., description="File path or URL")
    source_type: SourceType = Field(..., description="Type of source")
    
    @field_validator("source_type", mode="before")
    @classmethod
    def determine_source_type(cls, v: Any, info) -> SourceType:
        """Auto-determine source type from source string."""
        if isinstance(v, SourceType):
            return v
            
        source = info.data.get("source", "")
        if isinstance(source, str):
            parsed = urlparse(source)
            if parsed.scheme in ("http", "https"):
                return SourceType.WEB_URL
            else:
                return SourceType.LOCAL_FILE
        
        return SourceType.LOCAL_FILE


class DocumentMetadata(BaseModel):
    """Document metadata information."""
    
    filename: str = Field(..., description="Original filename")
    format: DocumentFormat = Field(..., description="Document format")
    size_bytes: Optional[int] = Field(None, description="File size in bytes")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    modified_at: Optional[datetime] = Field(None, description="Last modification timestamp")
    source: DocumentSource = Field(..., description="Document source information")
    checksum: Optional[str] = Field(None, description="File checksum (SHA-256)")
    
    @field_validator("format", mode="before")
    @classmethod
    def determine_format(cls, v: Any, info) -> DocumentFormat:
        """Auto-determine format from filename if not provided."""
        if isinstance(v, DocumentFormat):
            return v
            
        filename = info.data.get("filename", "")
        if isinstance(filename, str):
            extension = Path(filename).suffix.lower().lstrip(".")
            try:
                return DocumentFormat(extension)
            except ValueError:
                # Default to PDF if format cannot be determined
                return DocumentFormat.PDF
        
        return DocumentFormat.PDF


class CollectionRequest(BaseModel):
    """Request for document collection."""
    
    source: str = Field(..., description="File path or URL of document")
    destination_path: Path = Field(
        default=Path("./documents"),
        description="Destination directory for collected documents"
    )
    convert_to_markdown: bool = Field(
        default=True,
        description="Whether to convert document to markdown"
    )
    preserve_original: bool = Field(
        default=False,
        description="Whether to keep original file alongside markdown"
    )
    overwrite_existing: bool = Field(
        default=False,
        description="Whether to overwrite existing files"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata to attach"
    )
    
    @field_validator("destination_path", mode="before")
    @classmethod
    def ensure_path(cls, v: Any) -> Path:
        """Ensure destination_path is a Path object."""
        if isinstance(v, str):
            return Path(v)
        elif isinstance(v, Path):
            return v
        else:
            return Path("./documents")


class CollectionResult(BaseModel):
    """Result of document collection operation."""
    
    success: bool = Field(..., description="Whether collection was successful")
    source: str = Field(..., description="Original source path/URL")
    output_path: Optional[Path] = Field(None, description="Path to converted document")
    original_path: Optional[Path] = Field(None, description="Path to original document")
    metadata: Optional[DocumentMetadata] = Field(None, description="Document metadata")
    errors: List[str] = Field(default_factory=list, description="List of errors encountered")
    warnings: List[str] = Field(default_factory=list, description="List of warnings")
    processing_time_seconds: Optional[float] = Field(None, description="Processing time")
    
    @property
    def has_errors(self) -> bool:
        """Check if result has errors."""
        return len(self.errors) > 0
    
    @property
    def has_warnings(self) -> bool:
        """Check if result has warnings."""
        return len(self.warnings) > 0


class BatchCollectionRequest(BaseModel):
    """Request for batch document collection."""
    
    sources: List[str] = Field(..., description="List of file paths or URLs")
    destination_path: Path = Field(
        default=Path("./documents"),
        description="Destination directory for collected documents"
    )
    convert_to_markdown: bool = Field(
        default=True,
        description="Whether to convert documents to markdown"
    )
    preserve_original: bool = Field(
        default=False,
        description="Whether to keep original files alongside markdown"
    )
    overwrite_existing: bool = Field(
        default=False,
        description="Whether to overwrite existing files"
    )
    parallel_processing: bool = Field(
        default=True,
        description="Whether to process documents in parallel"
    )
    max_workers: int = Field(
        default=4,
        description="Maximum number of worker threads for parallel processing"
    )


class BatchCollectionResult(BaseModel):
    """Result of batch document collection operation."""
    
    total_requested: int = Field(..., description="Total number of documents requested")
    successful: int = Field(default=0, description="Number of successful collections")
    failed: int = Field(default=0, description="Number of failed collections")
    results: List[CollectionResult] = Field(
        default_factory=list,
        description="Individual collection results"
    )
    total_processing_time_seconds: Optional[float] = Field(
        None,
        description="Total processing time"
    )
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_requested == 0:
            return 0.0
        return (self.successful / self.total_requested) * 100.0
    
    @property
    def all_errors(self) -> List[str]:
        """Get all errors from individual results."""
        errors = []
        for result in self.results:
            errors.extend(result.errors)
        return errors
    
    @property
    def all_warnings(self) -> List[str]:
        """Get all warnings from individual results."""
        warnings = []
        for result in self.results:
            warnings.extend(result.warnings)
        return warnings
