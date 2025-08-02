"""Enhanced CLI tests to improve coverage."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, patch

from click.testing import CliRunner

# Add project root to sys.path for test discovery
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from document_collection.cli.main import (
    cli,
    collect,
    collect_batch,
    list_formats,
    mcp_server,
)
from document_collection.core.models import CollectionResult


class TestCLICommands:
    """Test CLI commands with enhanced coverage."""

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()

    def test_cli_version(self):
        """Test CLI version command."""
        result = self.runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Document Collection Tool" in result.output
        assert "collect" in result.output
        assert "collect-batch" in result.output
        assert "list-formats" in result.output
        assert "mcp-server" in result.output

    def test_collect_help(self):
        """Test collect command help."""
        result = self.runner.invoke(collect, ["--help"])
        assert result.exit_code == 0
        assert "Collect a single document" in result.output

    def test_collect_batch_help(self):
        """Test collect-batch command help."""
        result = self.runner.invoke(collect_batch, ["--help"])
        assert result.exit_code == 0
        assert "Collect multiple documents" in result.output

    def test_list_formats_command(self):
        """Test list-formats command execution."""
        result = self.runner.invoke(list_formats)
        assert result.exit_code == 0
        assert "Supported Document Formats" in result.output
        assert "PDF" in result.output
        assert "Word" in result.output
        assert "PowerPoint" in result.output
        assert "Excel" in result.output
        assert "Markdown" in result.output

    def test_mcp_server_help(self):
        """Test mcp-server command help."""
        result = self.runner.invoke(mcp_server, ["--help"])
        assert result.exit_code == 0
        assert "MCP (Model Context Protocol) server" in result.output
        assert "--transport" in result.output
        assert "--port" in result.output

    @patch("document_collection.cli.main.DocumentCollectionService")
    def test_collect_single_file_success(self, mock_service_class):
        """Test successful single file collection."""
        # Mock the service
        mock_service = AsyncMock()
        mock_service_class.return_value = mock_service

        # Mock successful collection result
        mock_result = CollectionResult(
            success=True,
            source="test.pdf",
            output_path=Path("/tmp/test.md"),
            original_path=Path("/tmp/test.pdf"),
            metadata=None,
            errors=[],
            warnings=[],
            processing_time_seconds=0.1,
        )
        mock_service.collect_document.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.runner.invoke(
                collect, ["test.pdf", "--destination", temp_dir, "--verbose"]
            )

            # Should exit successfully
            assert result.exit_code == 0

    @patch("document_collection.cli.main.DocumentCollectionService")
    def test_collect_single_file_failure(self, mock_service_class):
        """Test failed single file collection."""
        # Mock the service
        mock_service = AsyncMock()
        mock_service_class.return_value = mock_service

        # Mock failed collection result
        mock_result = CollectionResult(
            success=False,
            source="nonexistent.pdf",
            output_path=None,
            original_path=None,
            metadata=None,
            errors=["File not found"],
            warnings=[],
            processing_time_seconds=0.05,
        )
        mock_service.collect_document.return_value = mock_result

        result = self.runner.invoke(collect, ["nonexistent.pdf"])

        # Should exit with error code
        assert result.exit_code == 1

    @patch("document_collection.cli.main.DocumentCollectionService")
    def test_collect_quiet_mode(self, mock_service_class):
        """Test collect command in quiet mode."""
        # Mock the service
        mock_service = AsyncMock()
        mock_service_class.return_value = mock_service

        # Mock successful collection result
        mock_result = CollectionResult(
            success=True,
            source="test.pdf",
            output_path=Path("/tmp/test.md"),
            original_path=Path("/tmp/test.pdf"),
            metadata=None,
            errors=[],
            warnings=[],
            processing_time_seconds=0.1,
        )
        mock_service.collect_document.return_value = mock_result

        result = self.runner.invoke(collect, ["test.pdf", "--quiet"])

        # Should succeed but produce minimal output
        assert result.exit_code == 0

    @patch("document_collection.cli.main.DocumentCollectionService")
    def test_collect_with_all_options(self, mock_service_class):
        """Test collect command with all options."""
        # Mock the service
        mock_service = AsyncMock()
        mock_service_class.return_value = mock_service

        # Mock successful collection result
        mock_result = CollectionResult(
            success=True,
            source="test.pdf",
            output_path=Path("/tmp/test.md"),
            original_path=Path("/tmp/test.pdf"),
            metadata=None,
            errors=[],
            warnings=[],
            processing_time_seconds=0.1,
        )
        mock_service.collect_document.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.runner.invoke(
                collect,
                [
                    "test.pdf",
                    "--destination",
                    temp_dir,
                    "--no-convert",
                    "--preserve-original",
                    "--overwrite",
                    "--verbose",
                ],
            )

            assert result.exit_code == 0

    def test_collect_batch_basic(self):
        """Test collect-batch command basic functionality."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test1.pdf\ntest2.docx\n")
            f.flush()

            # Test with mock to avoid actual processing
            with patch(
                "document_collection.cli.main._collect_multiple_documents"
            ) as mock_collect:
                mock_collect.return_value = True

                result = self.runner.invoke(collect_batch, [f.name, "--verbose"])

                # Should handle the file list
                assert result.exit_code == 0

    def test_collect_batch_with_options(self):
        """Test collect-batch command with various options."""
        sources = ["test1.pdf", "test2.docx", "https://example.com/test3.pdf"]

        with patch(
            "document_collection.cli.main._collect_multiple_documents"
        ) as mock_collect:
            mock_collect.return_value = True

            with tempfile.TemporaryDirectory() as temp_dir:
                result = self.runner.invoke(
                    collect_batch,
                    [
                        *sources,
                        "--destination",
                        temp_dir,
                        "--no-convert",
                        "--preserve-original",
                        "--overwrite",
                        "--quiet",
                    ],
                )

                assert result.exit_code == 0

    def test_collect_batch_keyboard_interrupt(self):
        """Test collect-batch command keyboard interrupt handling."""
        sources = ["test1.pdf", "test2.docx"]

        with patch(
            "document_collection.cli.main._collect_multiple_documents"
        ) as mock_collect:
            mock_collect.side_effect = KeyboardInterrupt()

            result = self.runner.invoke(collect_batch, sources)

            # Should handle interrupt gracefully
            assert result.exit_code == 1

    def test_collect_batch_unexpected_error(self):
        """Test collect-batch command unexpected error handling."""
        sources = ["test1.pdf", "test2.docx"]

        with patch(
            "document_collection.cli.main._collect_multiple_documents"
        ) as mock_collect:
            mock_collect.side_effect = Exception("Unexpected error")

            result = self.runner.invoke(collect_batch, sources)

            # Should handle error gracefully
            assert result.exit_code == 1

    def test_collect_conflicting_flags(self):
        """Test collect command with conflicting verbose/quiet flags."""
        result = self.runner.invoke(collect, ["test.pdf", "--verbose", "--quiet"])

        # Should detect conflict and exit with error
        assert result.exit_code == 1
        assert "Cannot use both --quiet and --verbose" in result.output

    def test_collect_batch_conflicting_flags(self):
        """Test collect-batch command with conflicting verbose/quiet flags."""
        result = self.runner.invoke(
            collect_batch, ["test1.pdf", "--verbose", "--quiet"]
        )

        # Should detect conflict and exit with error
        assert result.exit_code == 1
        assert "Cannot use both --quiet and --verbose" in result.output

    @patch("document_collection.mcp_server.server.run_server")
    def test_mcp_server_stdio_transport(self, mock_run_server):
        """Test MCP server with stdio transport."""
        result = self.runner.invoke(mcp_server, ["--transport", "stdio"])

        assert result.exit_code == 0
        mock_run_server.assert_called_once()

    @patch("document_collection.mcp_server.server.run_server_http")
    def test_mcp_server_http_transport(self, mock_run_server_http):
        """Test MCP server with HTTP transport."""
        result = self.runner.invoke(
            mcp_server, ["--transport", "http", "--port", "9000"]
        )

        assert result.exit_code == 0
        mock_run_server_http.assert_called_once_with(port=9000)

    @patch("document_collection.mcp_server.server.run_server_http")
    def test_mcp_server_default_http_port(self, mock_run_server_http):
        """Test MCP server with HTTP transport using default port."""
        result = self.runner.invoke(mcp_server, ["--transport", "http"])

        assert result.exit_code == 0
        mock_run_server_http.assert_called_once_with(port=8000)

    def test_collect_invalid_source(self):
        """Test collect command with invalid source."""
        result = self.runner.invoke(collect, [""])

        # Should handle empty source
        assert result.exit_code != 0

    @patch("document_collection.cli.main.DocumentCollectionService")
    def test_collect_exception_handling(self, mock_service_class):
        """Test collect command exception handling."""
        # Mock service to raise exception
        mock_service = AsyncMock()
        mock_service_class.return_value = mock_service
        mock_service.collect_document.side_effect = Exception("Service error")

        result = self.runner.invoke(collect, ["test.pdf"])

        # Should handle exception gracefully
        assert result.exit_code == 1
