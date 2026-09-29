# India Road Accident Analytics — Project Specification

## Problem statement

Explore patterns in the provided accident-level road-safety CSV using its event timestamps, recorded locations, road/environment conditions, vehicle and driver categories, safety indicators, outcome counts, causes, and coordinates. Findings describe this file's records; the CSV alone does not establish complete national coverage or causal relationships.

## Objectives

- Inspect the original CSV and preserve it unchanged.
- Apply optional, transparent filters and extract compact time features.
- Validate identifiers, dates, categories, numeric measures, Boolean fields, and coordinates.
- Create a cleaned copy without imputing or fabricating values.
- Produce descriptive aggregates, analysis, figures, and a reproducible report.

## Dataset description

- **Active source:** `data/raw/india_road_accidents_dataset.csv`
- **Provided filename:** `india_road_accidents_dataset (2).csv`
- **Observed size:** 240 rows × 25 columns.
- **Granularity:** one row per recorded accident, identified by `accident_id`.
- **Observed period:** years 2021–2024 in the supplied file.
- **Source provenance:** supplied CSV. No source publication or representative sampling method is established by the file itself.
- **Exact source fields:** `accident_id`, `date_time`, `year`, `month`, `state_ut`, `district`, `road_type`, `weather`, `road_surface`, `lighting`, `vehicle_type`, `driver_age_group`, `driver_gender`, `speed_limit_kmph`, `estimated_speed_kmph`, `alcohol_involved`, `helmet_seatbelt_used`, `severity`, `fatalities`, `severe_injuries`, `minor_injuries`, `primary_cause`, `pedestrians_involved`, `latitude`, `longitude`.

## Mandatory eight stages

1. **Data Loading & Reading** — inspect the real file's dimensions, columns, rows, types, and accident-level granularity.
2. **Data Acquisition & Filtering** — demonstrate optional filters for year, State/UT, severity, fatal outcomes, pedestrians, alcohol, road type, and weather; keep all rows by default.
3. **Data Extraction** — map source fields into thematic groups and save a compact date/time feature table keyed by accident ID.
4. **Data Validation & Cleaning** — report missingness, duplicate rows/IDs, parse/domain problems, and save a cleaned copy without imputation.
5. **Data Aggregation & Representation** — save accident counts and recorded outcome totals by time, location, severity, conditions, and participant categories.
6. **Data Analysis** — calculate descriptive rankings, year/month patterns, recorded safety indicators, speed differences, and causes associated with fatal outcomes.
7. **Data Visualization** — generate labeled SVG charts from observed data.
8. **Results & Interpretation** — regenerate findings and limitations in a report, describing only the supplied records.

## Analysis questions

Which State/UT has the most recorded accidents and fatalities? Which severity, cause, and vehicle categories are most frequent? How do records vary by year, month, weather, lighting, and road type? How often are records marked alcohol-involved or pedestrian-involved? How do estimated speeds compare with listed limits? Which primary causes have the largest recorded fatality totals? Which driver age groups appear most often?

## Architecture and outputs

`data/raw/india_road_accidents_dataset.csv` → loader → optional acquisition filters → compact extracted calendar features and validated cleaned copy → aggregate tables and descriptive findings → SVG figures and `reports/RESULTS_SUMMARY.md`.

- `data/processed/extracted_accidents.csv`: accident ID plus derived date, hour, and month number.
- `data/processed/cleaned_accidents.csv`: validated/typed copy of the 25 source fields.
- `data/processed/aggregates/`: 19 CSV tables, including the required time, location, severity, injury/fatality, road, weather, lighting, vehicle, driver, cause, and safety summaries.
- `data/processed/pipeline_summary.json`: source dimensions, quality findings, output paths, and observations.
- `outputs/figures/`: generated SVG charts.
- `reports/RESULTS_SUMMARY.md`: calculated findings and interpretation limits.

## Derived measures

The extraction file derives `accident_date`, `accident_hour`, and calendar `month_number` from `date_time`. Aggregates calculate record counts, summed fatalities, severe injuries, minor injuries, nonfatal injuries (severe plus minor), Boolean-flagged record counts, and records where estimated speed is greater than the listed speed limit. These are descriptive calculations from source fields.

## Limitations

Only 240 supplied records are included. The CSV does not identify how records were selected, collected, or verified, so results must not be described as nationwide official statistics. A field named `primary_cause` is analyzed as a recorded category, not independently confirmed causation. Counts are not exposure-adjusted rates. The combined `helmet_seatbelt_used` field may apply differently by vehicle. Coordinates and category values are not independently verified.

## Reproducibility

Use Python 3.10 or newer. Install `requirements.txt`, run `python -m src.run_pipeline` or `python run_pipeline.py` from the repository root, then run `python audit_pipeline_outputs.py`. Both pipeline entry points use the same implementation and do not modify the raw CSV. The eight notebooks can be run in numerical order from the project root.
