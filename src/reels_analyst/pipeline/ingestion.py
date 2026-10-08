from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from reels_analyst.core.config import DATABASE_PATH
from reels_analyst.core.models import ReelRecord
from reels_analyst.pipeline.warehouse import connect


def ingest_csv(source_path: Path, database_path: Path = DATABASE_PATH) -> int:
    """Validate a CSV export and replace the raw warehouse table atomically."""
    frame = pd.read_csv(source_path).fillna(
        {"caption": "", "audio_name": "Original audio", "topic": "Uncategorized"}
    )
    records: list[dict] = []
    errors: list[str] = []
    for index, row in frame.iterrows():
        try:
            records.append(ReelRecord.model_validate(row.to_dict()).model_dump())
        except ValidationError as exc:
            errors.append(f"row {index + 2}: {exc.errors()[0]['msg']}")
    if errors:
        preview = "; ".join(errors[:5])
        raise ValueError(f"Input validation failed ({len(errors)} row(s)): {preview}")
    if not records:
        raise ValueError("The input contains no Reels.")

    clean = pd.DataFrame(records)
    with connect(database_path) as connection:
        connection.register("incoming_reels", clean)
        connection.execute("CREATE OR REPLACE TABLE raw_reels AS SELECT * FROM incoming_reels")
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS raw_reels_id ON raw_reels(reel_id)")
    return len(records)
