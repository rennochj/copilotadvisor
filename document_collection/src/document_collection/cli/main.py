"""Main CLI entry point for document collection."""

import asyncio
import sys
import time
from pathlib import Path

import click

from ..core.service import DocumentCollectionService


@click.group()
@click.version_option(version="1.0.0")
def cli() -> None:
    """Document Collection Tool - Collect and convert documents from local files or web URLs."""
    pass


@cli.command()
@click.argument("source", type=str)
@click.option(
    "--destination",
    "-d",
    type=click.Path(path_type=Path),
    default=Path("./documents"),
    help="Destination directory for collected documents (default: ./documents)",
)
@click.option(
    "--convert-to-markdown/--no-convert",
    default=True,
    help="Convert document to markdown format (default: true)",
)
@click.option(
    "--preserve-original",
    is_flag=True,
    help="Keep original file alongside markdown version",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Overwrite existing files without prompting",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress all output except errors",
)
def collect(
    source: str,
    destination: Path,
    convert_to_markdown: bool,
    preserve_original: bool,
    overwrite: bool,
    verbose: bool,
    quiet: bool,
) -> None:
    """
    Collect a single document from a file path or URL.

    SOURCE can be:
    - Local file path: /path/to/document.pdf
    - Web URL: https://example.com/document.pdf
    """
    if quiet and verbose:
        click.echo("Error: Cannot use both --quiet and --verbose flags", err=True)
        sys.exit(1)

    try:
        # Run the async collection
        result = asyncio.run(
            _collect_single_document(
                source=source,
                destination=destination,
                convert_to_markdown=convert_to_markdown,
                preserve_original=preserve_original,
                overwrite=overwrite,
                verbose=verbose,
                quiet=quiet,
            )
        )

        if not result:
            sys.exit(1)

    except KeyboardInterrupt:
        if not quiet:
            click.echo("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("sources", nargs=-1, required=True)
@click.option(
    "--destination",
    "-d",
    type=click.Path(path_type=Path),
    default=Path("./documents"),
    help="Destination directory for collected documents (default: ./documents)",
)
@click.option(
    "--convert-to-markdown/--no-convert",
    default=True,
    help="Convert documents to markdown format (default: true)",
)
@click.option(
    "--preserve-original",
    is_flag=True,
    help="Keep original files alongside markdown versions",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Overwrite existing files without prompting",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress all output except errors",
)
def collect_batch(
    sources: tuple[str, ...],
    destination: Path,
    convert_to_markdown: bool,
    preserve_original: bool,
    overwrite: bool,
    verbose: bool,
    quiet: bool,
) -> None:
    """
    Collect multiple documents from file paths or URLs.

    SOURCES can be multiple arguments:
    - Local files: /path/to/doc1.pdf /path/to/doc2.docx
    - Web URLs: https://example.com/doc1.pdf https://example.com/doc2.docx
    - Mixed: /path/to/local.pdf https://example.com/remote.docx
    """
    if quiet and verbose:
        click.echo("Error: Cannot use both --quiet and --verbose flags", err=True)
        sys.exit(1)

    try:
        # Run the async batch collection
        success = asyncio.run(
            _collect_multiple_documents(
                sources=list(sources),
                destination=destination,
                convert_to_markdown=convert_to_markdown,
                preserve_original=preserve_original,
                overwrite=overwrite,
                verbose=verbose,
                quiet=quiet,
            )
        )

        if not success:
            sys.exit(1)

    except KeyboardInterrupt:
        if not quiet:
            click.echo("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
def formats() -> None:
    """List supported document formats."""
    click.echo("Supported Document Formats:")
    click.echo("=" * 50)

    formats_info = [
        ("PDF", ".pdf", "Portable Document Format"),
        ("Word", ".docx", "Microsoft Word Document"),
        ("PowerPoint", ".pptx", "Microsoft PowerPoint Presentation"),
        ("Excel", ".xlsx", "Microsoft Excel Spreadsheet"),
        ("Markdown", ".md", "Markdown Document (processing/validation)"),
    ]

    for format_name, extension, description in formats_info:
        click.echo(f"{format_name:12} {extension:8} - {description}")


async def _collect_single_document(
    source: str,
    destination: Path,
    convert_to_markdown: bool,
    preserve_original: bool,
    overwrite: bool,
    verbose: bool,
    quiet: bool,
) -> bool:
    """Collect a single document with progress indication."""
    service = DocumentCollectionService()

    if not quiet:
        click.echo(f"Collecting document from: {source}")
        click.echo(f"Destination: {destination}")
        click.echo("Processing...", nl=False)

    start_time = time.time()
    result = await service.collect_document(
        source=source,
        destination_path=destination,
        convert_to_markdown=convert_to_markdown,
        preserve_original=preserve_original,
        overwrite_existing=overwrite,
    )
    end_time = time.time()

    if not quiet:
        click.echo(" Done!")

    if result.success:
        if not quiet:
            click.echo("✓ Successfully collected document")
            click.echo(f"  Output: {result.output_path}")
            if result.original_path and result.original_path != result.output_path:
                click.echo(f"  Original: {result.original_path}")
            click.echo(f"  Processing time: {end_time - start_time:.2f}s")

            if verbose and result.metadata:
                click.echo(f"  Filename: {result.metadata.filename}")
                click.echo(f"  Format: {result.metadata.format}")
                if result.metadata.size_bytes:
                    click.echo(f"  Size: {result.metadata.size_bytes} bytes")
        return True
    else:
        if not quiet:
            click.echo("✗ Failed to collect document")
            click.echo(f"  Processing time: {end_time - start_time:.2f}s")
            for error in result.errors:
                click.echo(f"  Error: {error}")
            for warning in result.warnings:
                click.echo(f"  Warning: {warning}")
        return False


async def _collect_multiple_documents(
    sources: list[str],
    destination: Path,
    convert_to_markdown: bool,
    preserve_original: bool,
    overwrite: bool,
    verbose: bool,
    quiet: bool,
) -> bool:
    """Collect multiple documents with progress indication."""
    service = DocumentCollectionService()

    if not quiet:
        click.echo(f"Collecting {len(sources)} documents")
        click.echo(f"Destination: {destination}")

    results = await service.collect_documents(
        sources=sources,
        destination_path=destination,
        convert_to_markdown=convert_to_markdown,
        preserve_original=preserve_original,
        overwrite_existing=overwrite,
    )

    # Summarize results
    successful = [r for r in results if r.success]
    failed = [r for r in results if not r.success]

    if not quiet:
        if successful:
            click.echo(f"✓ Successfully collected {len(successful)} documents")
            if verbose:
                for result in successful:
                    click.echo(f"  ✓ {result.source} → {result.output_path}")

        if failed:
            click.echo(f"✗ Failed to collect {len(failed)} documents")
            for result in failed:
                click.echo(f"  ✗ {result.source}")
                if verbose:
                    for error in result.errors:
                        click.echo(f"    Error: {error}")

    return len(failed) == 0


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
