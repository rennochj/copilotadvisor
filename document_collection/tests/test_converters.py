"""Tests for document converters."""

import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "document_collection" / "src")
)

import pytest

from document_collection.converters.excel_converter import ExcelConverter
from document_collection.converters.factory import ConverterFactory
from document_collection.converters.markdown_processor import MarkdownProcessor
from document_collection.converters.pdf_converter import PdfConverter
from document_collection.converters.powerpoint_converter import PowerPointConverter
from document_collection.converters.word_converter import WordConverter


class TestConverterFactory:
    """Test the converter factory."""

    def test_get_pdf_converter(self):
        """Test getting PDF converter."""
        converter = ConverterFactory.get_converter("document.pdf")
        assert isinstance(converter, PdfConverter)

    def test_get_word_converter(self):
        """Test getting Word converter."""
        converter = ConverterFactory.get_converter("document.docx")
        assert isinstance(converter, WordConverter)

    def test_get_powerpoint_converter(self):
        """Test getting PowerPoint converter."""
        converter = ConverterFactory.get_converter("presentation.pptx")
        assert isinstance(converter, PowerPointConverter)

    def test_get_excel_converter(self):
        """Test getting Excel converter."""
        converter = ConverterFactory.get_converter("spreadsheet.xlsx")
        assert isinstance(converter, ExcelConverter)

    def test_get_markdown_processor(self):
        """Test getting Markdown processor."""
        converter = ConverterFactory.get_converter("readme.md")
        assert isinstance(converter, MarkdownProcessor)

    def test_unsupported_format_raises_error(self):
        """Test that unsupported formats raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported file type"):
            ConverterFactory.get_converter("document.txt")


class TestPdfConverter:
    """Test PDF converter."""

    def test_can_convert_pdf(self):
        """Test PDF converter can handle PDF files."""
        converter = PdfConverter()
        assert converter.can_convert(Path("test.pdf"))
        assert not converter.can_convert(Path("test.docx"))

    def test_get_supported_formats(self):
        """Test PDF converter supported formats."""
        converter = PdfConverter()
        assert "pdf" in converter.get_supported_formats()

    @pytest.mark.asyncio
    async def test_convert_returns_output_path(self):
        """Test PDF convert method returns output path."""
        converter = PdfConverter()
        input_path = Path("test.pdf")
        output_path = Path("test.md")
        result = await converter.convert(input_path, output_path)
        assert result == output_path


class TestWordConverter:
    """Test Word converter."""

    def test_can_convert_docx(self):
        """Test Word converter can handle DOCX files."""
        converter = WordConverter()
        assert converter.can_convert(Path("test.docx"))
        assert not converter.can_convert(Path("test.pdf"))

    def test_get_supported_formats(self):
        """Test Word converter supported formats."""
        converter = WordConverter()
        assert "docx" in converter.get_supported_formats()

    @pytest.mark.asyncio
    async def test_convert_returns_output_path(self):
        """Test Word convert method returns output path."""
        converter = WordConverter()
        input_path = Path("test.docx")
        output_path = Path("test.md")
        result = await converter.convert(input_path, output_path)
        assert result == output_path


class TestPowerPointConverter:
    """Test PowerPoint converter."""

    def test_can_convert_pptx(self):
        """Test PowerPoint converter can handle PPTX files."""
        converter = PowerPointConverter()
        assert converter.can_convert(Path("test.pptx"))
        assert not converter.can_convert(Path("test.pdf"))

    def test_get_supported_formats(self):
        """Test PowerPoint converter supported formats."""
        converter = PowerPointConverter()
        assert "pptx" in converter.get_supported_formats()

    @pytest.mark.asyncio
    async def test_convert_returns_output_path(self):
        """Test PowerPoint convert method returns output path."""
        converter = PowerPointConverter()
        input_path = Path("test.pptx")
        output_path = Path("test.md")
        result = await converter.convert(input_path, output_path)
        assert result == output_path


class TestExcelConverter:
    """Test Excel converter."""

    def test_can_convert_xlsx(self):
        """Test Excel converter can handle XLSX files."""
        converter = ExcelConverter()
        assert converter.can_convert(Path("test.xlsx"))
        assert not converter.can_convert(Path("test.pdf"))

    def test_get_supported_formats(self):
        """Test Excel converter supported formats."""
        converter = ExcelConverter()
        assert "xlsx" in converter.get_supported_formats()

    @pytest.mark.asyncio
    async def test_convert_returns_output_path(self):
        """Test Excel convert method returns output path."""
        converter = ExcelConverter()
        input_path = Path("test.xlsx")
        output_path = Path("test.md")
        result = await converter.convert(input_path, output_path)
        assert result == output_path


class TestMarkdownProcessor:
    """Test Markdown processor."""

    def test_can_convert_md(self):
        """Test Markdown processor can handle MD files."""
        converter = MarkdownProcessor()
        assert converter.can_convert(Path("test.md"))
        assert not converter.can_convert(Path("test.pdf"))

    def test_get_supported_formats(self):
        """Test Markdown processor supported formats."""
        converter = MarkdownProcessor()
        assert "md" in converter.get_supported_formats()

    @pytest.mark.asyncio
    async def test_convert_returns_output_path(self):
        """Test Markdown convert method returns output path."""
        converter = MarkdownProcessor()
        input_path = Path("test.md")
        output_path = Path("test.md")
        result = await converter.convert(input_path, output_path)
        assert result == output_path
