from pathlib import Path

import typer

from reels_analyst.analytics.service import kpis
from reels_analyst.pipeline.ingestion import ingest_csv
from reels_analyst.pipeline.warehouse import build_views

app = typer.Typer(help="Ingest and analyze Instagram Reels performance exports.")


@app.command()
def ingest(file: Path = typer.Argument(..., exists=True, readable=True)) -> None:
    """Validate and load an Instagram export CSV."""
    count = ingest_csv(file)
    typer.echo(f"Loaded {count} Reels.")


@app.command()
def transform() -> None:
    """Build derived analytics views."""
    build_views()
    typer.echo("Analytics views are ready.")


@app.command()
def report() -> None:
    """Print account-level KPI snapshot."""
    for label, value in kpis().items():
        typer.echo(f"{label}: {value}")


if __name__ == "__main__":
    app()
