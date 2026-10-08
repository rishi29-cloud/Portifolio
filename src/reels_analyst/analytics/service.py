from pathlib import Path

from reels_analyst.core.config import DATABASE_PATH
from reels_analyst.pipeline.warehouse import connect


def _rows(query: str, database_path: Path = DATABASE_PATH) -> list[dict]:
    with connect(database_path) as connection:
        result = connection.execute(query).fetchdf()
    return result.to_dict(orient="records")


def kpis(database_path: Path = DATABASE_PATH) -> dict:
    values = _rows("SELECT * FROM account_kpis", database_path)
    if not values:
        return {"reels": 0, "plays": 0, "reach": 0, "engagement_rate": 0, "follows": 0}
    return values[0]


def top_reels(limit: int = 10, database_path: Path = DATABASE_PATH) -> list[dict]:
    return _rows(
        f"SELECT * FROM fact_reels ORDER BY engagement_rate DESC LIMIT {int(limit)}", database_path
    )


def performance_by(field: str, database_path: Path = DATABASE_PATH) -> list[dict]:
    allowed = {"topic", "publish_hour", "duration_bucket", "published_week"}
    if field not in allowed:
        raise ValueError(f"Unsupported breakdown: {field}")
    return _rows(
        f"""SELECT {field} AS dimension,
                   COUNT(*) AS reels,
                   ROUND(AVG(engagement_rate), 4) AS engagement_rate,
                   ROUND(AVG(follow_conversion_rate), 4) AS follow_conversion_rate,
                   SUM(reach) AS reach
            FROM fact_reels GROUP BY 1 ORDER BY engagement_rate DESC""",
        database_path,
    )
