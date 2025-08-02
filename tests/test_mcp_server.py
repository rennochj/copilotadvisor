import pytest
from src.document_collection.cli.main import mcp_server as mcp

@pytest.mark.asyncio
async def test_collect_document():
    result = await mcp.collect_document(url="https://example.com/document.pdf", output_dir="./documents")
    assert result["status"] == "success"
    assert "output_path" in result

@pytest.mark.asyncio
async def test_collect_batch():
    urls = ["https://example.com/doc1.pdf", "https://example.com/doc2.pdf"]
    result = await mcp.collect_batch(urls=urls, output_dir="./documents")
    assert result["status"] == "success"
    assert len(result["results"]) == len(urls)

@pytest.mark.asyncio
async def test_list_formats():
    result = await mcp.list_formats()
    assert result["status"] == "success"
    assert "formats" in result
    assert "PDF" in result["formats"]