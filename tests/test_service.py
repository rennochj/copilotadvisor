"""Tests for document collection service."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "document_collection" / "src"))

import pytest
from unittest.mock import AsyncMock, patch
from document_collection.core.service import DocumentCollectionService


class TestDocumentCollectionService:
    """Test document collection service."""
    
    def test_service_initialization(self):
        """Test service initializes correctly."""
        service = DocumentCollectionService()
        assert service.config is not None
        assert service.retriever_factory is not None
        assert service.converter_factory is not None
    
    @pytest.mark.asyncio
    async def test_collect_document_success(self):
        """Test successful document collection."""
        service = DocumentCollectionService()
        
        # Mock successful retrieval and conversion
        mock_retriever = AsyncMock()
        mock_retriever.retrieve.return_value = Path("/temp/document.pdf")
        
        mock_converter = AsyncMock()
        mock_converter.convert.return_value = Path("/output/document.md")
        mock_converter.can_convert.return_value = True
        
        with patch.object(service.retriever_factory, 'get_retriever', return_value=mock_retriever), \
             patch.object(service.converter_factory, 'get_converter', return_value=mock_converter), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.stat') as mock_stat:
            
            mock_stat.return_value.st_size = 1024
            mock_stat.return_value.st_mtime = 1234567890
            
            result = await service.collect_document(
                source="https://example.com/document.pdf",
                destination_path=Path("/output")
            )
            
            assert result.success is True
            assert result.source == "https://example.com/document.pdf"
            mock_retriever.retrieve.assert_called_once()
            mock_converter.convert.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_collect_document_retrieval_failure(self):
        """Test document collection with retrieval failure."""
        service = DocumentCollectionService()
        
        # Mock failed retrieval
        mock_retriever = AsyncMock()
        mock_retriever.retrieve.side_effect = Exception("Retrieval failed")
        
        with patch.object(service.retriever_factory, 'get_retriever', return_value=mock_retriever):
            result = await service.collect_document(
                source="https://example.com/nonexistent.pdf",
                destination_path=Path("/output")
            )
            
            assert result.success is False
            assert len(result.errors) > 0
            assert "Retrieval failed" in str(result.errors)
    
    @pytest.mark.asyncio
    async def test_collect_document_conversion_failure(self):
        """Test document collection with conversion failure."""
        service = DocumentCollectionService()
        
        # Mock successful retrieval but failed conversion
        mock_retriever = AsyncMock()
        mock_retriever.retrieve.return_value = Path("/temp/document.pdf")
        
        mock_converter = AsyncMock()
        mock_converter.convert.side_effect = Exception("Conversion failed")
        mock_converter.can_convert.return_value = True
        
        with patch.object(service.retriever_factory, 'get_retriever', return_value=mock_retriever), \
             patch.object(service.converter_factory, 'get_converter', return_value=mock_converter), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.stat') as mock_stat:
            
            mock_stat.return_value.st_size = 1024
            mock_stat.return_value.st_mtime = 1234567890
            
            result = await service.collect_document(
                source="https://example.com/document.pdf",
                destination_path=Path("/output")
            )
            
            assert result.success is False
            assert len(result.errors) > 0
            assert "Conversion failed" in str(result.errors)
    
    @pytest.mark.asyncio
    async def test_collect_documents_batch(self):
        """Test batch document collection."""
        service = DocumentCollectionService()
        
        # Mock successful operations for both documents
        mock_retriever = AsyncMock()
        mock_retriever.retrieve.side_effect = [
            Path("/temp/doc1.pdf"),
            Path("/temp/doc2.docx")
        ]
        
        mock_converter = AsyncMock()
        mock_converter.convert.side_effect = [
            Path("/output/doc1.md"),
            Path("/output/doc2.md")
        ]
        mock_converter.can_convert.return_value = True
        
        with patch.object(service.retriever_factory, 'get_retriever', return_value=mock_retriever), \
             patch.object(service.converter_factory, 'get_converter', return_value=mock_converter), \
             patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.stat') as mock_stat:
            
            mock_stat.return_value.st_size = 1024
            mock_stat.return_value.st_mtime = 1234567890
            
            results = await service.collect_documents(
                sources=["https://example.com/doc1.pdf", "/local/doc2.docx"],
                destination_path=Path("/output")
            )
            
            assert len(results) == 2
            assert all(result.success for result in results)
            assert mock_retriever.retrieve.call_count == 2
            assert mock_converter.convert.call_count == 2
