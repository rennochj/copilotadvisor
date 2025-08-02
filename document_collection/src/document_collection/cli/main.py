"""Main CLI entry point for document collection."""

import asyncio
import sys
import time
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ..core.service import DocumentCollectionService

# Initialize rich console
console = Console()


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
def list_formats() -> None:
    """List supported document formats."""
    table = Table(title="[bold blue]Supported Document Formats[/bold blue]")
    table.add_column("Format", style="cyan", no_wrap=True)
    table.add_column("Extension", style="magenta")
    table.add_column("Description", style="green")

    formats_info = [
        ("PDF", ".pdf", "Portable Document Format"),
        ("Word", ".docx", "Microsoft Word Document"),
        ("PowerPoint", ".pptx", "Microsoft PowerPoint Presentation"),
        ("Excel", ".xlsx", "Microsoft Excel Spreadsheet"),
        ("Markdown", ".md", "Markdown Document (processing/validation)"),
    ]

    for format_name, extension, description in formats_info:
        table.add_row(format_name, extension, description)

    console.print(table)


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
            console.print("✅ [bold green]Successfully collected document[/bold green]")
            console.print(f"  📄 Output: [blue]{result.output_path}[/blue]")
            if result.original_path and result.original_path != result.output_path:
                console.print(f"  📁 Original: [blue]{result.original_path}[/blue]")
            console.print(
                f"  ⏱️  Processing time: [yellow]{end_time - start_time:.2f}s[/yellow]"
            )

            if verbose and result.metadata:
                console.print(f"  📋 Filename: {result.metadata.filename}")
                console.print(f"  🔖 Format: {result.metadata.format}")
                if result.metadata.size_bytes:
                    console.print(f"  📏 Size: {result.metadata.size_bytes} bytes")
        return True
    else:
        if not quiet:
            console.print("❌ [bold red]Failed to collect document[/bold red]")
            console.print(
                f"  ⏱️  Processing time: [yellow]{end_time - start_time:.2f}s[/yellow]"
            )
            for error in result.errors:
                console.print(f"  🚨 Error: [red]{error}[/red]")
            for warning in result.warnings:
                console.print(f"  ⚠️  Warning: [yellow]{warning}[/yellow]")
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
        console.print(f"📦 [bold blue]Collecting {len(sources)} documents[/bold blue]")
        console.print(
            f"📁 [bold blue]Destination:[/bold blue] [blue]{destination}[/blue]"
        )

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
            console.print(
                f"✅ [bold green]Successfully collected {len(successful)} documents[/bold green]"
            )
            if verbose:
                for result in successful:
                    console.print(
                        f"  ✅ [green]{result.source}[/green] → [blue]{result.output_path}[/blue]"
                    )

        if failed:
            console.print(
                f"❌ [bold red]Failed to collect {len(failed)} documents[/bold red]"
            )
            for result in failed:
                console.print(f"  ❌ [red]{result.source}[/red]")
                if verbose:
                    for error in result.errors:
                        console.print(f"    🚨 Error: [red]{error}[/red]")

    return len(failed) == 0


@cli.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http"]),
    default="stdio",
    help="Transport type for MCP server (default: stdio)",
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Port for HTTP transport (default: 8000)",
)
def mcp_server(transport: str, port: int) -> None:
    """Run the MCP (Model Context Protocol) server for document collection."""
    from ..mcp_server.server import run_server, run_server_http

    console.print(
        "🚀 [bold blue]Starting Document Collection MCP Server...[/bold blue]"
    )
    console.print(f"🔗 [bold blue]Transport:[/bold blue] [cyan]{transport}[/cyan]")

    if transport == "http":
        console.print(f"🌐 [bold blue]Port:[/bold blue] [yellow]{port}[/yellow]")
        run_server_http(port=port)
    else:
        run_server()


def main() -> None:
    """Main entry point for the CLI."""
    cli()


__all__ = ["cli", "main"]

if __name__ == "__main__":
    main()
