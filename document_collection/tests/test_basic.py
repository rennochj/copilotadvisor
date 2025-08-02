"""Test basic imports and configuration."""

from pathlib import Path

import pytest

from document_collection.core.config import Configuration, get_config
from document_collection.core.models import (
    CollectionRequest,
    CollectionResult,
    DocumentFormat,
    SourceType,
)
from document_collection.core.service import DocumentCollectionService


def test_configuration_basic():
    """Test basic configuration functionality."""
    config = Configuration()
    assert config.get("destination_path") == "documents"
    assert config.max_workers > 0
    assert config.timeout > 0


def test_global_config():
    """Test global configuration access."""
    config = get_config()
    assert config is not None
    assert isinstance(config, Configuration)


def test_collection_request_creation():
    """Test CollectionRequest model creation."""
    request = CollectionRequest(source="test.pdf", destination_path=Path("./output"))
    assert request.source == "test.pdf"
    assert request.destination_path == Path("./output")
    assert request.preserve_original is False
    assert request.convert_to_markdown is True


def test_collection_result_creation():
    """Test CollectionResult model creation."""
    result = CollectionResult(
        success=True,
        source="test.pdf",
        output_path=Path("./output/test.md"),
        original_path=Path("./test.pdf"),
        metadata=None,
        processing_time_seconds=1.5,
    )
    assert result.success is True
    assert result.source == "test.pdf"
    assert result.output_path == Path("./output/test.md")
    assert result.processing_time_seconds == 1.5
    assert not result.has_errors
    assert not result.has_warnings


def test_document_collection_service_init():
    """Test DocumentCollectionService initialization."""
    service = DocumentCollectionService()
    assert service.config is not None
    assert isinstance(service.config, Configuration)


@pytest.mark.asyncio
async def test_document_collection_service_placeholder():
    """Test DocumentCollectionService placeholder implementation."""
    service = DocumentCollectionService()

    result = await service.collect_document(
        source="test.pdf", destination_path=Path("./output")
    )

    # Should return a failed result for placeholder implementation
    assert result.success is False
    assert result.source == "test.pdf"
    assert len(result.errors) > 0
    assert "Not implemented yet" in result.errors[0]


def test_document_format_enum():
    """Test DocumentFormat enum values."""
    assert DocumentFormat.PDF == "pdf"
    assert DocumentFormat.WORD == "docx"
    assert DocumentFormat.POWERPOINT == "pptx"
    assert DocumentFormat.EXCEL == "xlsx"
    assert DocumentFormat.MARKDOWN == "md"


def test_source_type_enum():
    """Test SourceType enum values."""
    assert SourceType.LOCAL_FILE == "local_file"
    assert SourceType.WEB_URL == "web_url"
