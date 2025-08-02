"""Tests for document retrievers."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "document_collection" / "src"))

import pytest
from unittest.mock import patch, MagicMock
from document_collection.retrievers.factory import RetrieverFactory
from document_collection.retrievers.local_retriever import LocalFileRetriever
from document_collection.retrievers.web_retriever import WebHttpRetriever


class TestRetrieverFactory:
    """Test the retriever factory."""
    
    def test_get_web_retriever_for_http_url(self):
        """Test getting web retriever for HTTP URL."""
        retriever = RetrieverFactory.get_retriever("http://example.com/document.pdf")
        assert isinstance(retriever, WebHttpRetriever)
    
    def test_get_web_retriever_for_https_url(self):
        """Test getting web retriever for HTTPS URL."""
        retriever = RetrieverFactory.get_retriever("https://example.com/document.pdf")
        assert isinstance(retriever, WebHttpRetriever)
    
    def test_get_local_retriever_for_file_path(self):
        """Test getting local retriever for file path."""
        retriever = RetrieverFactory.get_retriever("/path/to/document.pdf")
        assert isinstance(retriever, LocalFileRetriever)
    
    def test_get_local_retriever_for_relative_path(self):
        """Test getting local retriever for relative path."""
        retriever = RetrieverFactory.get_retriever("./document.pdf")
        assert isinstance(retriever, LocalFileRetriever)


class TestLocalFileRetriever:
    """Test local file retriever."""
    
    @pytest.mark.asyncio
    async def test_retrieve_success(self):
        """Test successful file retrieval."""
        retriever = LocalFileRetriever()
        
        # Mock file operations
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.is_file', return_value=True), \
             patch('shutil.copy2') as mock_copy:
            
            source = "/path/to/source.pdf"
            destination = Path("/path/to/dest")
            
            result = await retriever.retrieve(source, destination)
            
            # Should copy file to destination directory
            mock_copy.assert_called_once()
            assert result == destination / "source.pdf"
    
    @pytest.mark.asyncio
    async def test_retrieve_file_not_found(self):
        """Test file not found error."""
        retriever = LocalFileRetriever()
        
        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(Exception):  # Should raise RetrievalError
                await retriever.retrieve("/nonexistent/file.pdf", Path("/dest"))


class TestWebHttpRetriever:
    """Test web HTTP retriever."""
    
    @pytest.mark.asyncio
    async def test_retrieve_success(self):
        """Test successful web retrieval."""
        retriever = WebHttpRetriever()
        
        # Mock successful HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/pdf'}
        mock_response.content = b'fake pdf content'
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.get', return_value=mock_response), \
             patch('builtins.open', create=True) as mock_open:
            
            source = "https://example.com/document.pdf"
            destination = Path("/path/to/dest")
            
            result = await retriever.retrieve(source, destination)
            
            # Should save file to destination directory
            mock_open.assert_called()
            assert result == destination / "document.pdf"
    
    @pytest.mark.asyncio
    async def test_retrieve_http_error(self):
        """Test HTTP error during retrieval."""
        retriever = WebHttpRetriever()
        
        # Mock HTTP error response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        
        with patch('requests.get', return_value=mock_response):
            with pytest.raises(Exception):  # Should raise RetrievalError
                await retriever.retrieve("https://example.com/notfound.pdf", Path("/dest"))
