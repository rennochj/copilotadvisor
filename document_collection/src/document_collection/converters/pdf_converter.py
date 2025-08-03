"""PDF to Markdown converter implementation."""

from pathlib import Path
from typing import Any

from document_collection.core.interfaces import DocumentConverter


class PdfConverter(DocumentConverter):
    """Convert PDF documents to Markdown format with image extraction."""

    def can_convert(self, file_path: Path) -> bool:
        """Check if this converter can handle PDF files."""
        return str(file_path).lower().endswith(".pdf")

    def get_supported_formats(self) -> list[str]:
        """Return list of supported formats."""
        return ["pdf"]

    async def convert(self, input_path: Path, output_path: Path, **kwargs: Any) -> Path:
        """Convert PDF document to Markdown using pypdf with image extraction."""
        try:
            from pypdf import PdfReader

            # Read PDF document
            reader = PdfReader(str(input_path))

            # Create images directory
            images_dir = output_path.parent / "images"
            images_dir.mkdir(parents=True, exist_ok=True)

            # Extract text and images
            content_parts = [f"# {input_path.stem}\n"]
            content_parts.append("Converted from PDF document\n")

            image_counter = 1
            extracted_images = []

            # Process each page
            for page_num, page in enumerate(reader.pages, 1):
                # Extract text from page
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        content_parts.append(f"\n## Page {page_num}\n\n")
                        # Clean up text formatting
                        cleaned_text = self._clean_text(page_text)
                        content_parts.append(f"{cleaned_text}\n")
                except Exception:
                    # Continue if text extraction fails for this page
                    content_parts.append(f"\n## Page {page_num}\n\n")
                    content_parts.append("*Text extraction failed for this page.*\n")

                # Extract images from page
                try:
                    if hasattr(page, 'images'):
                        # Use a simpler approach to extract images
                        try:
                            images = list(page.images)
                            for image_obj in images:
                                try:
                                    # Get image data more safely
                                    if hasattr(image_obj, 'data'):
                                        image_data = image_obj.data
                                    else:
                                        continue

                                    # Create filename with page and image index
                                    new_filename = f"{input_path.stem}_page{page_num:03d}_image_{image_counter:03d}.png"
                                    image_path = images_dir / new_filename

                                    # Save image
                                    with open(image_path, 'wb') as img_file:
                                        img_file.write(image_data)

                                    extracted_images.append((page_num, new_filename))
                                    image_counter += 1

                                except Exception:
                                    # Skip this image if extraction fails
                                    continue
                        except Exception:
                            # Skip image extraction for this page if enumeration fails
                            pass
                except Exception:
                    # Continue if page image extraction fails
                    pass

            # Add extracted images section
            if extracted_images:
                content_parts.append(f"\n*This document contains {len(extracted_images)} extracted images stored in the `images/` directory.*\n")
                content_parts.append("\n## Extracted Images\n\n")
                for page_num, filename in extracted_images:
                    content_parts.append(f"![Image from Page {page_num}](images/{filename})\n\n")

            # Add document metadata
            content_parts.append("\n## Document Information\n\n")
            content_parts.append(f"- **Pages**: {len(reader.pages)}\n")
            if reader.metadata:
                if reader.metadata.title:
                    content_parts.append(f"- **Title**: {reader.metadata.title}\n")
                if reader.metadata.author:
                    content_parts.append(f"- **Author**: {reader.metadata.author}\n")
                if reader.metadata.subject:
                    content_parts.append(f"- **Subject**: {reader.metadata.subject}\n")
                if reader.metadata.creator:
                    content_parts.append(f"- **Creator**: {reader.metadata.creator}\n")

            # Write markdown content
            markdown_content = "\n".join(content_parts)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            return output_path

        except ImportError:
            # Fallback if pypdf is not available
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {input_path.stem}\n\nPDF conversion requires pypdf library.\n")
            return output_path
        except Exception as e:
            # Create error file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {input_path.stem}\n\nError converting PDF document: {str(e)}\n")
            return output_path

    def _clean_text(self, text: str) -> str:
        """Clean and format extracted text."""
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if line:
                # Remove multiple spaces
                line = ' '.join(line.split())
                cleaned_lines.append(line)

        # Join lines with proper spacing
        return '\n\n'.join(cleaned_lines)
