# Document Collection Tool

A unified tool and MCP server for collecting documents from local workstations and web sources, converting them to markdown format for architectural reviews.

## Features

- **Local Document Retrieval**: Access files from user's local workstation
- **Web Document Retrieval**: Download documents from web pages via HTTP
- **Multi-format Support**: Handle PDF, PowerPoint, Excel, Word, and HTML documents
- **Format Conversion**: Convert all documents to standardized markdown
- **MCP Server Integration**: Full Model Context Protocol server with 3 tools (collect_document, collect_batch, list_formats)
- **CLI Interface**: Comprehensive command-line tool for direct usage
- **Async Processing**: Concurrent document processing for better performance
- **Structured Logging**: JSON logging with contextual information and error tracking
- **Multiple Transports**: Support for stdio (MCP standard) and HTTP transports

## Supported Formats

- PDF documents
- Microsoft PowerPoint (.pptx)
- Microsoft Word (.docx)
- Microsoft Excel (.xlsx)
- Markdown (.md)

## Installation

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd document_collection

# Set up development environment
make setup

# Install in development mode
make dev-install
```

### Production Installation

```bash
pip install document-collection
```

## Usage

The Document Collection Tool provides multiple interfaces for collecting and processing documents:

### Command Line Interface

#### Installation & Setup

```bash
# Development installation with uv (recommended)
git clone <repository>
cd document_collection
uv sync

# Or install with pip
pip install -e .

# Verify installation
collect-doc --help
```

#### Single Document Collection

```bash
# Basic usage - collect from local file
collect-doc collect /path/to/document.pdf

# Collect from web URL with authentication
collect-doc collect https://example.com/protected/document.pdf

# Custom destination directory
collect-doc collect document.pdf --destination ./my-documents

# Skip markdown conversion (keep original format processing)
collect-doc collect document.pdf --no-markdown

# Keep both original and processed files
collect-doc collect document.pdf --preserve-original

# Overwrite existing files without prompting
collect-doc collect document.pdf --overwrite

# Verbose output for debugging
collect-doc collect document.pdf --verbose

# Quiet mode (errors only)
collect-doc collect document.pdf --quiet
```

#### Batch Document Collection

```bash
# Multiple documents as arguments
collect-doc collect-batch doc1.pdf doc2.docx https://example.com/doc3.pptx

# From file list (one URL/path per line)
echo -e "document1.pdf\nhttps://example.com/doc2.docx" > sources.txt
collect-doc collect-batch sources.txt

# Batch with all options
collect-doc collect-batch --destination ./output \
                         --preserve-original \
                         --overwrite \
                         --verbose \
                         *.pdf *.docx

# Process large batches with progress tracking
collect-doc collect-batch --quiet large_document_list.txt
```

#### Utility Commands

```bash
# List all supported document formats
collect-doc list-formats

# Start MCP server for integration
collect-doc mcp-server

# MCP server with HTTP transport
collect-doc mcp-server --transport http --port 8000
```

#### Advanced CLI Usage

```bash
# Complex workflow example
collect-doc collect-batch \
    --destination ./processed_docs \
    --preserve-original \
    --verbose \
    "https://example.com/report1.pdf" \
    "https://example.com/presentation.pptx" \
    "./local_document.docx" \
    "./spreadsheet.xlsx"

# Error handling and recovery
collect-doc collect problematic_doc.pdf --verbose 2> errors.log

# Integration with other tools
find ./documents -name "*.pdf" | xargs collect-doc collect-batch --quiet
```

### Python API

#### Basic Service Usage

```python
import asyncio
from pathlib import Path
from document_collection.core.service import DocumentCollectionService

async def basic_collection():
    service = DocumentCollectionService()
    
    # Collect single document
    result = await service.collect_document(
        source="https://example.com/document.pdf",
        destination_path=Path("./documents"),
        convert_to_markdown=True,
        preserve_original=False,
        overwrite_existing=False
    )
    
    if result.success:
        print(f"✅ Collected: {result.output_path}")
        print(f"📊 Processing time: {result.processing_time_seconds:.2f}s")
        if result.metadata:
            print(f"📄 Metadata: {result.metadata}")
    else:
        print(f"❌ Failed: {', '.join(result.errors)}")
        if result.warnings:
            print(f"⚠️ Warnings: {', '.join(result.warnings)}")

# Run the example
asyncio.run(basic_collection())
```

#### Advanced Service Usage

```python
import asyncio
from pathlib import Path
from document_collection.core.service import DocumentCollectionService
from document_collection.core.config import DocumentCollectionConfig

async def advanced_collection():
    # Custom configuration
    config = DocumentCollectionConfig(
        output_directory=Path("./custom_output"),
        convert_to_markdown=True,
        preserve_original_files=True,
        overwrite_existing_files=True,
        max_concurrent_downloads=5,
        request_timeout_seconds=30
    )
    
    service = DocumentCollectionService(config=config)
    
    # Batch collection with progress tracking
    sources = [
        "https://example.com/doc1.pdf",
        "./local_document.docx",
        "https://example.com/presentation.pptx"
    ]
    
    results = []
    for source in sources:
        print(f"Processing: {source}")
        result = await service.collect_document(source)
        results.append(result)
        
        # Process result
        if result.success:
            print(f"  ✅ Success: {result.output_path}")
        else:
            print(f"  ❌ Failed: {', '.join(result.errors)}")
    
    # Summary
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]
    
    print(f"\n📊 Summary: {len(successful)} successful, {len(failed)} failed")
    
    return results

# Run advanced example
asyncio.run(advanced_collection())
```

#### Working with Different Document Types

```python
async def process_various_formats():
    service = DocumentCollectionService()
    
    # PDF document
    pdf_result = await service.collect_document(
        "https://example.com/report.pdf"
    )
    
    # Word document  
    word_result = await service.collect_document(
        "./presentation.docx"
    )
    
    # PowerPoint presentation
    ppt_result = await service.collect_document(
        "https://example.com/slides.pptx"
    )
    
    # Excel spreadsheet
    excel_result = await service.collect_document(
        "./data.xlsx"
    )
    
    # Markdown file (pass-through processing)
    md_result = await service.collect_document(
        "https://raw.githubusercontent.com/user/repo/README.md"
    )
    
    results = [pdf_result, word_result, ppt_result, excel_result, md_result]
    
    for result in results:
        print(f"Source: {result.source}")
        print(f"Status: {'✅ Success' if result.success else '❌ Failed'}")
        if result.metadata:
            print(f"Type: {result.metadata.get('document_type', 'Unknown')}")
        print("---")

asyncio.run(process_various_formats())
```
        print(f"Document collected: {result.output_path}")
    else:
        print(f"Collection failed: {result.errors}")

# Run the async function
asyncio.run(collect_document())
```

### Make Integration

```bash
# Set up development environment
make setup

# Run all tests
make test

# Run linting and type checking
make lint

# Generate coverage report
make coverage

# Collect a document using make (if implemented)
make collect-doc FILE=/path/to/document.pdf

# Clean build artifacts
make clean
```
collect-doc /path/to/document.pdf

# Collect from a URL
collect-doc https://example.com/document.pdf

# Specify destination directory
collect-doc /path/to/document.pdf --dest ./my-documents
```

### Make Targets

```bash
# Collect a single document
make collect-doc FILE=/path/to/document.pdf

# Collect multiple documents
make collect-docs FILES='/path/doc1.pdf /path/doc2.docx'
```

### MCP Server

The tool provides a Model Context Protocol (MCP) server that exposes document collection functionality as MCP tools. This enables integration with MCP-compatible clients like GitHub Copilot Chat, Claude Desktop, and other AI assistants.

#### Starting the MCP Server

```bash
# Start MCP server with stdio transport (default, for MCP clients)
collect-doc mcp-server

# Or using Python module directly
python -m document_collection.cli.main mcp-server

# Start with HTTP transport for web integration
collect-doc mcp-server --transport http --port 8000

# Development mode with uv
uv run python -m document_collection.cli.main mcp-server
```

#### Available MCP Tools

The MCP server exposes three tools:

1. **collect_document** - Collect a single document from a URL
   ```json
   {
     "url": "https://example.com/document.pdf",
     "output_dir": "output",
     "format_override": "markdown"
   }
   ```

2. **collect_batch** - Collect multiple documents from a list of URLs
   ```json
   {
     "urls": ["https://example.com/doc1.pdf", "https://example.com/doc2.docx"],
     "output_dir": "output",
     "format_override": "markdown"
   }
   ```

3. **list_formats** - List all supported document formats
   ```json
   {}
   ```

#### Integration with GitHub Copilot Chat

To integrate with GitHub Copilot Chat, add the MCP server to your copilot configuration:

```json
{
  "mcpServers": {
    "document-collection": {
      "command": "uv",
      "args": ["run", "python", "-m", "document_collection.cli.main", "mcp-server"],
      "env": {}
    }
  }
}
```

#### Integration with Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "document-collection": {
      "command": "python",
      "args": ["-m", "document_collection.cli.main", "mcp-server"]
    }
  }
}
```

#### MCP Server Features

- **Async Operations**: Full async support for concurrent document processing
- **Error Handling**: Comprehensive error reporting with detailed messages
- **Structured Responses**: JSON responses with success indicators, file lists, and metadata
- **Logging**: Structured logging with contextual information for debugging
- **Transport Options**: Support for both stdio (MCP standard) and HTTP transports
- **Format Support**: Same document format support as CLI (PDF, DOCX, PPTX, XLSX, HTML)

#### Example MCP Usage

Once the MCP server is running and configured with your AI assistant, you can use natural language to collect documents:

> "Please collect the PDF document from https://example.com/report.pdf and convert it to markdown"

> "Collect all these documents: https://site1.com/doc1.pdf, https://site2.com/doc2.docx, and save them to the 'reports' folder"

> "What document formats can you process?"

The MCP server will handle the requests, process the documents, and return structured results with file paths, success status, and any error messages.

### Example MCP Configuration Files

#### JSON Configuration Example
```json
{
  "mcpServers": {
    "document-collection": {
      "command": "uv",
      "args": ["run", "python", "-m", "document_collection.cli.main", "mcp-server"],
      "env": {
        "DOCUMENT_COLLECTION_DEST": "./custom-documents"
      }
    }
  }
}
```

#### YAML Configuration Example
```yaml
mcpServers:
  document-collection:
    command: uv
    args:
      - run
      - python
      - -m
      - document_collection.cli.main
      - mcp-server
    env:
      DOCUMENT_COLLECTION_DEST: ./custom-documents
```

#### TOML Configuration Example
```toml
[mcpServers.document-collection]
command = "uv"
args = ["run", "python", "-m", "document_collection.cli.main", "mcp-server"]
[mcpServers.document-collection.env]
DOCUMENT_COLLECTION_DEST = "./custom-documents"
```

## Configuration

Default destination directory: `./documents`

You can override this by:
- Using the `--dest` CLI option
- Setting the `DOCUMENT_COLLECTION_DEST` environment variable
- Creating a configuration file

## Development

### Running Tests

```bash
make test
```

### Code Quality

```bash
# Run linting
make lint

# Format code
make format

# Type checking
make type-check
```

### Development Workflow

```bash
# Run all quality checks
make dev
```

## Architecture

The tool is organized into several modules:

- `core/`: Core business logic and data models
- `retrievers/`: Document retrieval implementations
- `converters/`: Format conversion implementations
- `cli/`: Command-line interface
- `mcp_server/`: MCP server implementation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks: `make dev`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
