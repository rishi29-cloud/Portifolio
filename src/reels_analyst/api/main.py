from fastapi import FastAPI, HTTPException, Query

from reels_analyst.analytics.service import kpis, performance_by, top_reels

app = FastAPI(
    title="Reels Analyst API",
    version="0.1.0",
    description="Read-only analytics API over the local Reels warehouse.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/kpis")
def get_kpis() -> dict:
    return kpis()


@app.get("/v1/reels/top")
def get_top_reels(limit: int = Query(default=10, ge=1, le=100)) -> list[dict]:
    return top_reels(limit)


@app.get("/v1/performance/{dimension}")
def get_performance(dimension: str) -> list[dict]:
    try:
        return performance_by(dimension)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
