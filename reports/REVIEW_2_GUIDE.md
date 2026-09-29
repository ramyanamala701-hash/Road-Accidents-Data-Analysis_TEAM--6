# Capstone Review-2 Guide

The project follows the required eight stages using the 240-row, 25-column accident-level CSV at `data/raw/india_road_accidents_dataset.csv`. Describe findings as patterns observed in the supplied records. The file does not establish complete official national coverage or causal evidence.

## Pipeline flow

Raw CSV → loading → optional filtering → compact feature extraction → validation/cleaning → aggregation → descriptive analysis → figures → results report.

## Eight stages

1. **Data Loading & Reading:** inspect actual dimensions, source fields, dtypes, sample rows, and basic information.
2. **Data Acquisition & Filtering:** demonstrate real subsets by year, State/UT, severity, fatality, pedestrian/alcohol flags, road type, and weather; default processing retains all records.
3. **Data Extraction:** group source fields thematically and save derived date, hour, and month number keyed by `accident_id`.
4. **Data Validation & Cleaning:** report missing values, duplicate IDs/rows, invalid dates, year/month consistency, numeric ranges, Boolean values, coordinates, and severity. Preserve missingness; do not impute.
5. **Data Aggregation & Representation:** save clear CSV tables for counts and recorded outcomes across time, geography, conditions, severity, participants, cause, and safety flags.
6. **Data Analysis:** answer descriptive questions about highest recorded counts, category frequency, time patterns, flags, speed comparison, and fatal outcomes by recorded cause.
7. **Data Visualization:** generate SVG charts using only this CSV's values.
8. **Results & Interpretation:** write computed results, limitations, and conclusion to `reports/RESULTS_SUMMARY.md`.

## Interpretation guidance

- A `primary_cause` field is the dataset's label, not an independent causal finding.
- Higher counts in a State/UT or category mean more records in this file, not necessarily higher population-adjusted risk.
- `helmet_seatbelt_used` combines concepts whose applicability may depend on vehicle type.
- Collection, sampling, and verification details are not documented in the supplied file. Do not describe results as comprehensive nationwide official statistics.

## Running and outputs

Run `python -m src.run_pipeline` or `python run_pipeline.py` from the project root. The pipeline writes `cleaned_accidents.csv`, compact `extracted_accidents.csv`, 19 tables under `data/processed/aggregates/`, SVGs under `outputs/figures/`, metadata under `data/processed/pipeline_summary.json`, and the results report. Run `python audit_pipeline_outputs.py` to check the project.
