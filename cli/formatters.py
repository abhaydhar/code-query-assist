from rich.console import Console
from rich.table import Table

console = Console()


def format_response(query, results):
    table = Table(title=f"Results for: {query}")
    table.add_column("Type", style="cyan")
    table.add_column("Content", style="magenta")

    for res in results:
        table.add_row("Code", res)

    console.print(table)