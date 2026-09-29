# Processed data

Generated from the active raw CSV by `src/run_pipeline.py`:

- `cleaned_accidents.csv`: typed/validated copy of source fields; no imputation.
- `extracted_accidents.csv`: compact ID/date/hour/year/month/month-number table.
- `aggregates/`: named descriptive count and outcome tables.
- `pipeline_summary.json`: dimensions, quality checks, output paths, and observations.

Regenerate these files by running `python -m src.run_pipeline` from the project root. The pipeline removes stale aggregate tables before saving current summaries.
