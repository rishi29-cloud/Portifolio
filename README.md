# Reels Analyst

An end-to-end Instagram Reels analytics project built for a portfolio showcase. It turns exported account insights into a clean analytical model, exposes metrics through a FastAPI service, and provides an interactive Streamlit dashboard.

> This is an **unofficial analytics implementation**. It accepts CSV exports or data retrieved by a separately configured, authorized connector. It does not scrape Instagram or bypass Meta permissions.

## What it answers

- Which Reels earn the most reach, plays, engagement and followers?
- What hooks, formats, topics, durations and publishing slots perform best?
- Where is the retention drop-off? Which posts are candidates to repurpose?
- How has performance changed week over week?

## Architecture

```text
CSV export / authorized connector
            |
            v
  Validation + normalization (Pydantic)
            |
            v
 DuckDB warehouse ----> SQL metric views ----> FastAPI
            |                                      |
            +-------------------------------> Streamlit dashboard
```

## Stack

Python 3.11+, DuckDB, Pandas, Pydantic, FastAPI, Streamlit, Plotly, pytest, Ruff, Docker and GitHub Actions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python scripts/generate_sample_data.py
reels-analyst ingest data/raw/reels.csv
reels-analyst transform
uvicorn reels_analyst.api.main:app --reload
# in a second terminal
streamlit run dashboard.py
```

Open `http://localhost:8000/docs` for the API and `http://localhost:8501` for the dashboard.

### Static browser dashboard

The root-level `index.html`, `styles.css`, and `script.js` form a lightweight, dependency-free portfolio interface. With the API running, serve the project from a second terminal:

```bash
python -m http.server 5500
```

Then visit `http://localhost:5500`. The browser dashboard calls the local FastAPI service and renders the same warehouse metrics.

## Input contract

Place a CSV at `data/raw/reels.csv`. Required columns are:

```text
reel_id,published_at,caption,format,duration_seconds,plays,reach,likes,comments,
saves,shares,profile_visits,follows,avg_watch_seconds,completion_rate
```

Optional columns: `audio_name`, `topic`, `cover_url`. Timestamps must be ISO-8601. Percentages may be supplied as `0.42` or `42`.

## Project layout

```text
src/reels_analyst/      # application and analytics package
sql/                    # reproducible warehouse views
scripts/                # demo-data generator
tests/                  # unit + API tests
dashboard.py            # stakeholder-facing dashboard
data/raw/               # source exports (gitignored)
data/processed/         # DuckDB warehouse (gitignored)
```

## Commands

| Command | Purpose |
| --- | --- |
| `reels-analyst ingest data/raw/reels.csv` | validate and load raw Reel data |
| `reels-analyst transform` | build analytical views |
| `reels-analyst report` | print account KPI snapshot |
| `pytest` | run test suite |
| `ruff check .` | lint |

## Data model and metric definitions

The warehouse contains a `fact_reels` view with derived metrics. Engagement rate is `(likes + comments + saves + shares) / reach`; follow conversion is `follows / reach`; and average watch percentage is `avg_watch_seconds / duration_seconds`. Each denominator is guarded against zero.

The project includes generated sample data only—never commit exports containing personal or account-sensitive data.

## Docker

```bash
docker compose up --build
```

This starts the API on port 8000 and dashboard on port 8501. Run ingestion inside the API container before browsing the dashboard if you are using your own export.

## Showcase ideas

For a strong GitHub presentation, add screenshots from the dashboard, pin this repository, and write a short case study describing one decision you made from the data (for example, shifting publishing time after finding a higher follow-conversion rate).
