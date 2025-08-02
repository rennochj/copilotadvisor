"""Document Collection Package

A unified tool and MCP server for collecting documents from local workstations
and web sources, converting them to markdown format for architectural reviews.
"""

__version__ = "0.1.0"
__author__ = "Architecture Advisor"
__description__ = "Document collection and conversion tool for architectural reviews"

from .core.models import CollectionRequest, CollectionResult, DocumentMetadata
from .core.service import DocumentCollectionService

__all__ = [
    "DocumentCollectionService",
    "CollectionRequest",
    "CollectionResult",
    "DocumentMetadata",
]
