"""MCP Server implementation for document collection.

This module i# Create FastMCP server instance
mcp = FastMCP(name="Document Collection Server")ents an MCP (Model Context Protocol) server that provides
document collection tools accessible via the MCP interface. It uses the official
MCP Python SDK with FastMCP for server implementation.
"""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import structlog
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from ..core.service import DocumentCollectionService

# Configure structured logging
logger = structlog.get_logger(__name__)

# Define a type alias for the decorator
Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


class CollectDocumentRequest(BaseModel):
    """Request model for single document collection."""

    url: str = Field(description="URL of the document to collect")
    output_dir: str = Field(
        default="output", description="Output directory for collected document"
    )
    format_override: str | None = Field(
        default=None, description="Force specific output format (markdown, html, text)"
    )


class CollectBatchRequest(BaseModel):
    """Request model for batch document collection."""

    urls: list[str] = Field(description="List of URLs to collect")
    output_dir: str = Field(
        default="output", description="Output directory for collected documents"
    )
    format_override: str | None = Field(
        default=None, description="Force specific output format for all documents"
    )


class CollectionResult(BaseModel):
    """Result model for document collection operations."""

    success: bool = Field(description="Whether the operation was successful")
    message: str = Field(description="Status message")
    collected_files: list[str] = Field(
        default_factory=list, description="List of successfully collected files"
    )
    failed_urls: list[str] = Field(
        default_factory=list, description="List of URLs that failed to collect"
    )
    errors: list[str] = Field(
        default_factory=list, description="List of error messages"
    )


class FormatInfo(BaseModel):
    """Information about supported file formats."""

    format_name: str = Field(description="Name of the format")
    description: str = Field(description="Description of the format")
    file_extensions: list[str] = Field(description="Supported file extensions")


# Create FastMCP server instance
mcp = FastMCP(name="Document Collection Server")


@mcp.tool()
async def collect_document(
    url: str, output_dir: str = "output", format_override: str | None = None
) -> dict[str, Any]:
    """Collect a single document from the specified URL.

    Args:
        url: URL of the document to collect
        output_dir: Output directory for the collected document (default: "output")
        format_override: Force specific output format (markdown, html, text)

    Returns:
        Dictionary containing collection results and status information
    """
    logger.info("MCP collect_document called", url=url, output_dir=output_dir)

    try:
        # Initialize the document collection service
        service = DocumentCollectionService()

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Collect the document
        result = await service.collect_document(
            source=url, destination_path=output_path, format_override=format_override
        )

        if result.success:
            logger.info(
                "Document collected successfully",
                url=url,
                output_path=str(result.output_path) if result.output_path else None,
            )
            return CollectionResult(
                success=True,
                message=f"Successfully collected document from {url}",
                collected_files=[str(result.output_path)] if result.output_path else [],
                failed_urls=[],
                errors=[],
            ).model_dump()
        else:
            logger.error("Document collection failed", url=url, errors=result.errors)
            return CollectionResult(
                success=False,
                message=f"Failed to collect document from {url}",
                collected_files=[],
                failed_urls=[url],
                errors=result.errors if result.errors else ["Unknown error"],
            ).model_dump()

    except Exception as e:
        error_msg = f"Unexpected error collecting document: {str(e)}"
        logger.error(
            "Unexpected error in collect_document", url=url, error=str(e), exc_info=True
        )
        return CollectionResult(
            success=False,
            message=error_msg,
            collected_files=[],
            failed_urls=[url],
            errors=[error_msg],
        ).model_dump()


@mcp.tool()
async def collect_batch(
    urls: list[str], output_dir: str = "output", format_override: str | None = None
) -> dict[str, Any]:
    """Collect multiple documents from the specified URLs.

    Args:
        urls: List of URLs to collect documents from
        output_dir: Output directory for collected documents (default: "output")
        format_override: Force specific output format for all documents

    Returns:
        Dictionary containing batch collection results and status information
    """
    logger.info("MCP collect_batch called", url_count=len(urls), output_dir=output_dir)

    try:
        # Initialize the document collection service
        service = DocumentCollectionService()

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Collect documents in batch
        results = await service.collect_documents(
            sources=urls, destination_path=output_path, format_override=format_override
        )

        # Process results
        collected_files = []
        failed_urls = []
        errors = []

        for result in results:
            if result.success and result.output_path:
                collected_files.append(str(result.output_path))
            else:
                failed_urls.append(result.source)
                if result.errors:
                    errors.extend(
                        [f"{result.source}: {error}" for error in result.errors]
                    )

        success_count = len(collected_files)
        total_count = len(urls)

        logger.info(
            "Batch collection completed",
            total=total_count,
            success=success_count,
            failed=len(failed_urls),
        )

        return CollectionResult(
            success=success_count > 0,  # Success if at least one document collected
            message=f"Collected {success_count}/{total_count} documents successfully",
            collected_files=collected_files,
            failed_urls=failed_urls,
            errors=errors,
        ).model_dump()

    except Exception as e:
        error_msg = f"Unexpected error in batch collection: {str(e)}"
        logger.error(
            "Unexpected error in collect_batch",
            url_count=len(urls),
            error=str(e),
            exc_info=True,
        )
        return CollectionResult(
            success=False,
            message=error_msg,
            collected_files=[],
            failed_urls=urls,
            errors=[error_msg],
        ).model_dump()


@mcp.tool()
async def list_formats() -> dict[str, Any]:
    """List all supported document formats and their capabilities.

    Returns:
        Dictionary containing information about supported formats
    """
    logger.info("MCP list_formats called")

    try:
        # Define supported formats based on the converters in the system
        formats = [
            FormatInfo(
                format_name="pdf",
                description="Portable Document Format - Extract text from PDF files",
                file_extensions=[".pdf"],
            ).model_dump(),
            FormatInfo(
                format_name="docx",
                description="Microsoft Word Document - Extract text and content from Word files",
                file_extensions=[".docx", ".doc"],
            ).model_dump(),
            FormatInfo(
                format_name="pptx",
                description="Microsoft PowerPoint Presentation - Extract text and slide content",
                file_extensions=[".pptx", ".ppt"],
            ).model_dump(),
            FormatInfo(
                format_name="xlsx",
                description="Microsoft Excel Spreadsheet - Extract data from Excel files",
                file_extensions=[".xlsx", ".xls"],
            ).model_dump(),
            FormatInfo(
                format_name="html",
                description="HyperText Markup Language - Process web pages and HTML documents",
                file_extensions=[".html", ".htm"],
            ).model_dump(),
            FormatInfo(
                format_name="markdown",
                description="Markdown format - Convert documents to Markdown",
                file_extensions=[".md", ".markdown"],
            ).model_dump(),
        ]

        logger.info("Format list retrieved", format_count=len(formats))

        return {
            "formats": formats,
            "total_formats": len(formats),
            "message": f"Found {len(formats)} supported formats",
        }

    except Exception as e:
        error_msg = f"Error retrieving format information: {str(e)}"
        logger.error("Error in list_formats", error=str(e), exc_info=True)
        return {
            "formats": [],
            "total_formats": 0,
            "message": error_msg,
            "error": error_msg,
        }


def run_server() -> None:
    """Run the MCP server with stdio transport.

    This is the main entry point for running the MCP server.
    Uses stdio transport by default for compatibility with MCP clients.
    """
    logger.info("Starting Document Collection MCP Server")

    try:
        # Run with stdio transport (default for MCP)
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error("Server error", error=str(e), exc_info=True)
        raise


def run_server_http(port: int = 8000) -> None:
    """Run the MCP server with HTTP transport.

    Args:
        port: Port number for HTTP server (default: 8000)
    """
    logger.info("Starting Document Collection MCP Server (HTTP)", port=port)

    try:
        # Run with streamable HTTP transport
        # Note: Port configuration may need to be handled differently
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logger.info("HTTP server shutdown requested")
    except Exception as e:
        logger.error("HTTP server error", error=str(e), exc_info=True)
        raise


if __name__ == "__main__":
    # Configure structlog for better logging
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Run the server
    run_server()
