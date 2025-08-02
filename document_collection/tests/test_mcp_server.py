"""Tests for MCP Server functionality."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from document_collection.mcp_server.server import (
    collect_batch,
    collect_document,
    list_formats,
    mcp,
)


class TestMCPServer:
    """Test cases for the MCP server functionality."""

    @pytest.mark.asyncio
    async def test_collect_document_success(self) -> None:
        """Test successful single document collection."""
        # Mock the DocumentCollectionService
        mock_service = Mock()
        mock_result = Mock()
        mock_result.success = True
        mock_result.output_path = "/output/test.md"
        mock_result.errors = []
        mock_service.collect_document = AsyncMock(return_value=mock_result)

        with patch(
            "document_collection.mcp_server.server.DocumentCollectionService",
            return_value=mock_service,
        ):
            result = await collect_document(
                url="https://example.com/test.pdf", output_dir="output"
            )

        assert result["success"] is True
        assert (
            result["message"]
            == "Successfully collected document from https://example.com/test.pdf"
        )
        assert result["collected_files"] == ["/output/test.md"]
        assert result["failed_urls"] == []
        assert result["errors"] == []

    @pytest.mark.asyncio
    async def test_collect_document_failure(self) -> None:
        """Test failed single document collection."""
        # Mock the DocumentCollectionService
        mock_service = Mock()
        mock_result = Mock()
        mock_result.success = False
        mock_result.output_path = None
        mock_result.errors = ["Failed to download document"]
        mock_service.collect_document = AsyncMock(return_value=mock_result)

        with patch(
            "document_collection.mcp_server.server.DocumentCollectionService",
            return_value=mock_service,
        ):
            result = await collect_document(
                url="https://example.com/nonexistent.pdf", output_dir="output"
            )

        assert result["success"] is False
        assert "Failed to collect document" in result["message"]
        assert result["collected_files"] == []
        assert result["failed_urls"] == ["https://example.com/nonexistent.pdf"]
        assert result["errors"] == ["Failed to download document"]

    @pytest.mark.asyncio
    async def test_collect_batch_success(self) -> None:
        """Test successful batch document collection."""
        # Mock the DocumentCollectionService
        mock_service = Mock()

        # Create mock results
        mock_result1 = Mock()
        mock_result1.success = True
        mock_result1.output_path = "/output/test1.md"
        mock_result1.source = "https://example.com/test1.pdf"
        mock_result1.errors = []

        mock_result2 = Mock()
        mock_result2.success = True
        mock_result2.output_path = "/output/test2.md"
        mock_result2.source = "https://example.com/test2.pdf"
        mock_result2.errors = []

        mock_service.collect_documents = AsyncMock(
            return_value=[mock_result1, mock_result2]
        )

        with patch(
            "document_collection.mcp_server.server.DocumentCollectionService",
            return_value=mock_service,
        ):
            result = await collect_batch(
                urls=["https://example.com/test1.pdf", "https://example.com/test2.pdf"],
                output_dir="output",
            )

        assert result["success"] is True
        assert "Collected 2/2 documents successfully" in result["message"]
        assert len(result["collected_files"]) == 2
        assert result["failed_urls"] == []
        assert result["errors"] == []

    @pytest.mark.asyncio
    async def test_collect_batch_partial_failure(self) -> None:
        """Test batch collection with some failures."""
        # Mock the DocumentCollectionService
        mock_service = Mock()

        # Create mock results - one success, one failure
        mock_result1 = Mock()
        mock_result1.success = True
        mock_result1.output_path = "/output/test1.md"
        mock_result1.source = "https://example.com/test1.pdf"
        mock_result1.errors = []

        mock_result2 = Mock()
        mock_result2.success = False
        mock_result2.output_path = None
        mock_result2.source = "https://example.com/test2.pdf"
        mock_result2.errors = ["Download failed"]

        mock_service.collect_documents = AsyncMock(
            return_value=[mock_result1, mock_result2]
        )

        with patch(
            "document_collection.mcp_server.server.DocumentCollectionService",
            return_value=mock_service,
        ):
            result = await collect_batch(
                urls=["https://example.com/test1.pdf", "https://example.com/test2.pdf"],
                output_dir="output",
            )

        assert result["success"] is True  # Success if at least one document collected
        assert "Collected 1/2 documents successfully" in result["message"]
        assert len(result["collected_files"]) == 1
        assert len(result["failed_urls"]) == 1
        assert result["failed_urls"] == ["https://example.com/test2.pdf"]
        assert len(result["errors"]) == 1

    @pytest.mark.asyncio
    async def test_list_formats(self) -> None:
        """Test listing supported formats."""
        result = await list_formats()

        assert result["total_formats"] == 6
        assert "formats" in result
        assert len(result["formats"]) == 6

        # Check that expected formats are present
        format_names = [f["format_name"] for f in result["formats"]]
        expected_formats = ["pdf", "docx", "pptx", "xlsx", "html", "markdown"]

        for expected_format in expected_formats:
            assert expected_format in format_names

        # Check structure of first format
        first_format = result["formats"][0]
        assert "format_name" in first_format
        assert "description" in first_format
        assert "file_extensions" in first_format
        assert isinstance(first_format["file_extensions"], list)

    @pytest.mark.asyncio
    async def test_collect_document_exception_handling(self) -> None:
        """Test exception handling in collect_document."""
        # Mock the DocumentCollectionService to raise an exception
        mock_service = Mock()
        mock_service.collect_document = AsyncMock(
            side_effect=Exception("Unexpected error")
        )

        with patch(
            "document_collection.mcp_server.server.DocumentCollectionService",
            return_value=mock_service,
        ):
            result = await collect_document(
                url="https://example.com/test.pdf", output_dir="output"
            )

        assert result["success"] is False
        assert "Unexpected error" in result["message"]
        assert result["collected_files"] == []
        assert result["failed_urls"] == ["https://example.com/test.pdf"]
        assert len(result["errors"]) == 1

    @pytest.mark.asyncio
    async def test_collect_batch_exception_handling(self) -> None:
        """Test exception handling in collect_batch."""
        # Mock the DocumentCollectionService to raise an exception
        mock_service = Mock()
        mock_service.collect_documents = AsyncMock(
            side_effect=Exception("Service error")
        )

        with patch(
            "document_collection.mcp_server.server.DocumentCollectionService",
            return_value=mock_service,
        ):
            result = await collect_batch(
                urls=["https://example.com/test.pdf"], output_dir="output"
            )

        assert result["success"] is False
        assert "Unexpected error" in result["message"]
        assert result["collected_files"] == []
        assert result["failed_urls"] == ["https://example.com/test.pdf"]
        assert len(result["errors"]) == 1

    def test_mcp_server_instance(self) -> None:
        """Test that MCP server instance is properly configured."""
        assert mcp.name == "Document Collection Server"
        # FastMCP doesn't have a description attribute, so we just verify the server exists
        assert mcp is not None
