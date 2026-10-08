from pathlib import Path

import duckdb

from reels_analyst.core.config import DATABASE_PATH, SQL_DIR


def connect(database_path: Path = DATABASE_PATH) -> duckdb.DuckDBPyConnection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(database_path))


def build_views(database_path: Path = DATABASE_PATH) -> None:
    """Apply idempotent analytical SQL models in filename order."""
    with connect(database_path) as connection:
        for sql_file in sorted(SQL_DIR.glob("*.sql")):
            connection.execute(sql_file.read_text())
