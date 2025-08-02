# copilotadvisor

A frameowrk for providing guidance and advice for building solutions

## Document Collection Tool Usage

### CLI Commands

#### Collect a Document
```bash
uv run python -m document_collection.cli.main collect <document_url>
```

#### Run MCP Server (stdio transport for MCP clients)
```bash
uv run python -m document_collection.cli.main mcp-server
```

#### Run MCP Server (HTTP transport on port 8000)
```bash
uv run python -m document_collection.cli.main mcp-server --transport http --port 8000
```

### Features
- Supports PDF, DOCX, PPTX, XLSX, and Markdown formats.
- Converts documents to standardized Markdown for architectural reviews.
- Provides CLI and MCP server interfaces for document collection.

### Requirements
- Python 3.13+
- Dependencies: `structlog`, `rich`, `mcp`, `pyyaml`.

### Examples
#### Collect a Batch of Documents
```bash
uv run python -m document_collection.cli.main collect-batch <batch_file>
```

#### List Supported Formats
```bash
uv run python -m document_collection.cli.main formats
```
