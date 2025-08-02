"""ConverterManager for batch and pipeline conversion."""

from pathlib import Path

from document_collection.converters.factory import ConverterFactory


class ConverterManager:
    """Manages document conversion operations."""

    def __init__(self) -> None:
        self.factory = ConverterFactory()

    async def convert_batch(self, sources: list[str], destination: Path) -> list[Path]:
        results = []
        for source in sources:
            converter = self.factory.get_converter(source)
            input_path = Path(source)
            result = await converter.convert(input_path, destination)
            results.append(result)
        return results
