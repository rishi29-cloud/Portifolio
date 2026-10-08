.PHONY: demo ingest transform test lint run-api run-dashboard

demo:
	python scripts/generate_sample_data.py
	python -m reels_analyst.cli ingest data/raw/reels.csv
	python -m reels_analyst.cli transform

ingest:
	python -m reels_analyst.cli ingest data/raw/reels.csv

transform:
	python -m reels_analyst.cli transform

test:
	pytest

lint:
	ruff check .

run-api:
	uvicorn reels_analyst.api.main:app --reload

run-dashboard:
	streamlit run dashboard.py
