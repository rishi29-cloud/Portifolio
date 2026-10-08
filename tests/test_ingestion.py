from pathlib import Path

import pandas as pd
import pytest

from reels_analyst.pipeline.ingestion import ingest_csv
from reels_analyst.pipeline.warehouse import build_views


def valid_row() -> dict:
    return {
        "reel_id": "abc",
        "published_at": "2026-01-01T10:00:00",
        "caption": "hello",
        "format": "reel",
        "duration_seconds": 30,
        "plays": 110,
        "reach": 100,
        "likes": 10,
        "comments": 2,
        "saves": 3,
        "shares": 1,
        "profile_visits": 5,
        "follows": 2,
        "avg_watch_seconds": 18,
        "completion_rate": 55,
    }


def test_ingestion_normalizes_percentages_and_builds_views(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    database = tmp_path / "warehouse.duckdb"
    pd.DataFrame([valid_row()]).to_csv(source, index=False)

    assert ingest_csv(source, database) == 1
    build_views(database)

    import duckdb

    row = (
        duckdb.connect(str(database))
        .execute("SELECT completion_rate, engagement_rate FROM fact_reels")
        .fetchone()
    )
    assert row == (0.55, 0.16)


def test_ingestion_rejects_invalid_duration(tmp_path: Path) -> None:
    invalid = valid_row() | {"duration_seconds": 0}
    source = tmp_path / "bad.csv"
    pd.DataFrame([invalid]).to_csv(source, index=False)
    with pytest.raises(ValueError, match="Input validation failed"):
        ingest_csv(source, tmp_path / "warehouse.duckdb")
