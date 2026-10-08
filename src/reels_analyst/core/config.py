from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "reels.csv"
DATABASE_PATH = DATA_DIR / "processed" / "reels_analytics.duckdb"
SQL_DIR = PROJECT_ROOT / "sql"
