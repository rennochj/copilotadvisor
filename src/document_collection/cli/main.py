from rich.console import Console
from rich.progress import Progress

console = Console()

# Example usage in CLI commands
def collect_document(url: str, output_dir: str):
    console.print("[bold green]Starting document collection...[/bold green]")
    with Progress() as progress:
        task = progress.add_task("[cyan]Collecting document...", total=100)
        for _ in range(10):
            progress.update(task, advance=10)
    console.print("[bold green]Document collection completed successfully![/bold green]")

# Similar enhancements can be applied to other CLI commands like collect_batch and list_formats.