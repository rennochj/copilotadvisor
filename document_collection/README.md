# Document Collection Tool

A unified tool and MCP server for collecting documents from local workstations and web sources, converting them to markdown format for architectural reviews.

## Features

- **Local Document Retrieval**: Access files from user's local workstation
- **Web Document Retrieval**: Download documents from web pages via HTTP
- **Multi-format Support**: Handle PDF, PowerPoint, Excel, Word, and Markdown
- **Format Conversion**: Convert all documents to standardized markdown
- **MCP Server Integration**: Provide Model Context Protocol server interface
- **CLI Interface**: Command-line tool for direct usage
- **Make Integration**: Support invocation as make targets

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

### Command Line Interface

```bash
# Collect a single document
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

The tool provides an MCP server that can be integrated with GitHub Copilot Chat:

```bash
# Start MCP server
python -m document_collection.mcp_server
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
