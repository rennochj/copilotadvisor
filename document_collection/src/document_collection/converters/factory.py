"""ConverterFactory for selecting appropriate converter."""

from document_collection.converters.excel_converter import ExcelConverter
from document_collection.converters.markdown_processor import MarkdownProcessor
from document_collection.converters.pdf_converter import PdfConverter
from document_collection.converters.powerpoint_converter import PowerPointConverter
from document_collection.converters.word_converter import WordConverter


class ConverterFactory:
    """Factory to instantiate appropriate converter based on file type."""

    @staticmethod
    def get_converter(
        source: str,
    ) -> (
        PdfConverter
        | WordConverter
        | PowerPointConverter
        | ExcelConverter
        | MarkdownProcessor
    ):
        """Get appropriate converter based on file extension."""
        if source.lower().endswith(".pdf"):
            return PdfConverter()
        if source.lower().endswith(".docx"):
            return WordConverter()
        if source.lower().endswith(".pptx"):
            return PowerPointConverter()
        if source.lower().endswith(".xlsx"):
            return ExcelConverter()
        if source.lower().endswith(".md"):
            return MarkdownProcessor()
        raise ValueError(f"Unsupported file type: {source}")
