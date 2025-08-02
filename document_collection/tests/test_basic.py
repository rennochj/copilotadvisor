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


def test_configuration_basic() -> None:
    """Test basic configuration functionality."""
    config = Configuration()
    assert config.get("destination_path") == "documents"
    assert config.max_workers > 0
    assert config.timeout > 0


def test_global_config() -> None:
    """Test global configuration access."""
    config = get_config()
    assert config is not None
    assert isinstance(config, Configuration)


def test_collection_request_creation() -> None:
    """Test CollectionRequest model creation."""
    request = CollectionRequest(source="test.pdf", destination_path=Path("./output"))
    assert request.source == "test.pdf"
    assert request.destination_path == Path("./output")
    assert request.preserve_original is False
    assert request.convert_to_markdown is True


def test_collection_result_creation() -> None:
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


def test_document_collection_service_init() -> None:
    """Test DocumentCollectionService initialization."""
    service = DocumentCollectionService()
    assert service.config is not None
    assert isinstance(service.config, Configuration)


@pytest.mark.asyncio
async def test_document_collection_service_implementation() -> None:
    """Test DocumentCollectionService implementation."""
    service = DocumentCollectionService()

    # Test with non-existent file
    result = await service.collect_document(
        source="nonexistent.pdf", destination_path=Path("./output")
    )

    # Should return a failed result because file doesn't exist
    assert result.success is False
    assert result.source == "nonexistent.pdf"
    assert len(result.errors) > 0
    assert "File not found" in result.errors[0] or "No such file" in result.errors[0]


@pytest.mark.asyncio
async def test_document_collection_service_with_actual_file() -> None:
    """Test DocumentCollectionService with an actual file."""
    from tempfile import NamedTemporaryFile

    service = DocumentCollectionService()

    # Create a temporary test file with a supported format
    with NamedTemporaryFile(mode="w", suffix=".md", delete=False) as temp_file:
        temp_file.write("# Test Document\n\nThis is a test markdown document.")
        temp_file_path = temp_file.name

    try:
        result = await service.collect_document(
            source=temp_file_path,
            destination_path=Path("./test_output"),
            convert_to_markdown=False,
        )

        # Should succeed
        assert result.success is True
        assert result.source == temp_file_path
        assert result.output_path is not None
        assert len(result.errors) == 0

    finally:
        # Clean up
        import os

        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_document_format_enum() -> None:
    """Test DocumentFormat enum values."""
    assert DocumentFormat.PDF.value == "pdf"
    assert DocumentFormat.WORD.value == "docx"
    assert DocumentFormat.POWERPOINT.value == "pptx"
    assert DocumentFormat.EXCEL.value == "xlsx"
    assert DocumentFormat.MARKDOWN.value == "md"


def test_source_type_enum() -> None:
    """Test SourceType enum values."""
    assert SourceType.LOCAL_FILE.value == "local_file"
    assert SourceType.WEB_URL.value == "web_url"


def test_function_name() -> None:
    """Test enum comparison logic."""
    # Test DocumentFormat enum usage
    for format_value in [
        DocumentFormat.PDF,
        DocumentFormat.WORD,
        DocumentFormat.POWERPOINT,
    ]:
        if format_value == DocumentFormat.PDF:
            # Handle PDF format
            assert format_value.value == "pdf"
        elif format_value == DocumentFormat.WORD:
            # Handle Word format
            assert format_value.value == "docx"
        else:
            # Handle other formats
            assert format_value in [
                DocumentFormat.POWERPOINT,
                DocumentFormat.EXCEL,
                DocumentFormat.MARKDOWN,
            ]

    # Test SourceType enum usage
    for source_type in [SourceType.LOCAL_FILE, SourceType.WEB_URL]:
        if source_type == SourceType.LOCAL_FILE:
            # Handle local file source
            assert source_type.value == "local_file"
        elif source_type == SourceType.WEB_URL:
            # Handle web URL source
            assert source_type.value == "web_url"
        else:
            # Handle other source types (none exist currently)
            pass
