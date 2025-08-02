import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "document_collection" / "src")
)

from unittest.mock import AsyncMock, patch

import pytest
from click.testing import CliRunner

from document_collection.cli.main import cli
from document_collection.core.models import CollectionResult, DocumentMetadata


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_collection_result():
    """Create a mock successful collection result."""
    from datetime import datetime

    from document_collection.core.models import (
        DocumentFormat,
        DocumentSource,
        SourceType,
    )

    return CollectionResult(
        success=True,
        source="https://example.com/document.pdf",
        output_path=Path("./documents/document.md"),
        original_path=Path("./documents/document.pdf"),
        metadata=DocumentMetadata(
            filename="document.pdf",
            format=DocumentFormat.PDF,
            size_bytes=1024,
            created_at=datetime.now(),
            modified_at=datetime.now(),
            source=DocumentSource(
                source="https://example.com/document.pdf",
                source_type=SourceType.WEB_URL,
            ),
            checksum="abc123",
        ),
        errors=[],
        warnings=[],
        processing_time_seconds=1.5,
    )


def test_collect_document_command_success(runner, mock_collection_result):
    """Test successful document collection."""
    with patch(
        "document_collection.cli.main.DocumentCollectionService"
    ) as mock_service:
        mock_instance = AsyncMock()
        mock_service.return_value = mock_instance
        mock_instance.collect_document.return_value = mock_collection_result

        result = runner.invoke(cli, ["collect", "https://example.com/document.pdf"])
        assert result.exit_code == 0
        assert "Successfully collected document" in result.output


def test_formats_command(runner):
    """Test the list-formats command."""
    result = runner.invoke(cli, ["list-formats"])
    assert result.exit_code == 0
    assert "Supported Document Formats" in result.output
    assert "PDF" in result.output
    assert "Word" in result.output


def test_invalid_command(runner):
    result = runner.invoke(cli, ["invalid-command"])
    assert result.exit_code != 0
    assert "Error: No such command" in result.output
