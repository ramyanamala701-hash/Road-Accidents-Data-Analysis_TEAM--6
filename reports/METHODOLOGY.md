# Methodology

## Source and scope

The active input is the user-provided `data/raw/india_road_accidents_dataset.csv` (240 accident-level records, 25 columns). The project has no independent documentation of sampling, collection, or verification; findings are confined to this file.

## Processing

1. Load and inspect the source without writing to it.
2. Apply only explicitly requested optional filters; the normal run includes every row.
3. Normalize the field names for internal processing and extract compact date, hour, and month-number features keyed by accident ID.
4. Report missing values, duplicate rows and IDs, date/year/month consistency, numeric ranges, Boolean values, and selected categories. Invalid typed/domain values become missing in the processed copy and remain counted in the quality report. No imputation is performed. Exact duplicate rows are removed from the processed copy; repeated accident IDs are flagged and retained for review.
5. Sum recorded accident, injury, fatality, and Boolean-flag measures by the documented categories.
6. Calculate descriptive rankings and speed-limit comparisons. A cause label is treated as a recorded attribute and any fatality comparison as association only.
7. Generate SVG graphics directly from the actual output tables and records.
8. Write `reports/RESULTS_SUMMARY.md` and `pipeline_summary.json` from the current run.

## Validation boundaries

Speed limits are flagged outside 1–180 km/h and estimated speeds outside 0–300 km/h. Fatality/injury counts must be non-negative. Coordinates are checked against the valid latitude/longitude ranges for Earth. Severity, month, and gender are checked against the categories present in the supplied schema. These simple checks identify implausible values; they do not certify correctness or source authenticity.

## Reproducibility

Run either `python -m src.run_pipeline` or `python run_pipeline.py` from the project root. The raw CSV is read-only input; the pipeline recreates processed tables, aggregates, figures, and the report. `python audit_pipeline_outputs.py` reports schema, record quality, required outputs, and repository consistency.
