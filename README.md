# India Road Accident Analytics

## Project Overview

An eight-stage Review-2 project that explores the records in a supplied accident-level CSV. The workflow validates the 25 source fields, creates compact date features and a cleaned copy, calculates descriptive summaries, generates SVG charts, and writes a results report.

## Problem Statement

Road accident records can be described across time, location, severity, road/environment, vehicle/driver, and recorded safety/cause fields. The provided CSV supports descriptive comparisons within its rows. It does not by itself show why accidents occurred or establish official nationwide coverage.

## Objectives

- Preserve the uploaded source and make processing reproducible.
- Inspect, filter optionally, validate, and clean records without invented replacement values.
- Analyze recorded counts, injury/fatality totals, and descriptive category patterns.
- Communicate findings without causal or representativeness claims unsupported by the file.

## Dataset

The active file is `data/raw/india_road_accidents_dataset.csv`, copied from the user-provided `india_road_accidents_dataset (2).csv`. It has **240 rows and 25 columns**, with one recorded accident per row and observed years 2021–2024. Its fields cover ID/time; State/UT, district, and coordinates; road, weather, surface, and lighting; vehicle and driver categories; speed values; safety flags; severity and injury/fatality counts; and recorded primary cause. The complete field list is in [`reports/DATA_DICTIONARY.md`](reports/DATA_DICTIONARY.md).

The CSV does not document its sampling or verification method. The project therefore describes only the records in this file and does not claim they are complete official nationwide statistics.

## Eight-Stage Review-2 Pipeline

1. **Data Loading & Reading** — show dimensions, fields, first rows, types, and basic information.
2. **Data Acquisition & Filtering** — demonstrate optional year, location, severity, fatal, pedestrian, alcohol, road, and weather filters.
3. **Data Extraction** — map source fields by theme and derive a compact date/time table.
4. **Data Validation & Cleaning** — check missingness, duplicate IDs/rows, types, dates, domain values, and save a cleaned copy without imputing.
5. **Data Aggregation & Representation** — create descriptive CSV summaries across required categories and recorded outcomes.
6. **Data Analysis** — calculate frequency rankings and observed associations, including fatal outcomes by recorded primary cause.
7. **Data Visualization** — save labeled charts based only on the provided records.
8. **Results & Interpretation** — regenerate findings, limitations, and conclusion in the report.

## Project Structure

```text
india-road-accident-analytics/
├── 01_Data_Loading_and_Reading/       # Stage 1 notebook and README
├── 02_Data_Acquisition_and_Filtering/ # Stage 2 notebook and README
├── 03_Data_Extraction/                # Stage 3 notebook and README
├── 04_Data_Validation_and_Cleaning/   # Stage 4 notebook and README
├── 05_Data_Aggregation_and_Representation/
├── 06_Data_Analysis/
├── 07_Data_Visualization/
├── 08_Results_and_Interpretation/
├── data/raw/                          # User-provided CSV
├── data/processed/                    # Cleaned/extracted data, aggregates, summary
├── outputs/figures/                   # Generated SVG charts
├── outputs/models/                    # No model is currently produced
├── reports/                           # Methodology, results, guide, dictionary
├── notebooks/                         # Stage notebooks are in numbered folders
├── src/                               # Reusable pipeline modules
├── PROJECT_SPEC.md
├── audit_pipeline_outputs.py
├── run_pipeline.py
├── README.md
└── requirements.txt
```

## Installation

From the project root, install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Pipeline

Both commands run the same eight-stage pipeline from the repository root:

```bash
python -m src.run_pipeline
```

```bash
python run_pipeline.py
```

## Running Notebooks

Open the eight `.ipynb` files in their numbered stage folders and run them in order from the project root. The notebooks inspect actual values and call the same `src/` functions used by the pipeline.

## Outputs

- Compact extracted time features and cleaned records: `data/processed/`
- Category and outcome aggregates: `data/processed/aggregates/`
- SVG charts: `outputs/figures/`
- Run metadata and quality checks: `data/processed/pipeline_summary.json`
- Calculated findings: `reports/RESULTS_SUMMARY.md`

## Results

Findings are regenerated from the active CSV every time the pipeline runs. See [`reports/RESULTS_SUMMARY.md`](reports/RESULTS_SUMMARY.md) for observed counts and rankings. The report explicitly describes this file's records and avoids causal and nationwide-statistics claims.

## Limitations

The file contains 240 records, and its selection, collection, and verification method are not established by its contents. Recorded causes and conditions are descriptive labels, not proof of causation. Counts are not exposure-adjusted rates. The `helmet_seatbelt_used` field combines two safety-device concepts, applicability can depend on vehicle type, and coordinates/categories have not been independently validated.

## Reproducibility

Keep the supplied CSV at `data/raw/india_road_accidents_dataset.csv`, install dependencies, and run either pipeline command. Outputs are rebuilt from the source; raw CSV values are not changed. Run `python audit_pipeline_outputs.py` for a file/schema/data-quality/output audit. Consult [`PROJECT_SPEC.md`](PROJECT_SPEC.md), [`reports/DATA_DICTIONARY.md`](reports/DATA_DICTIONARY.md), and [`CONTRIBUTING.md`](CONTRIBUTING.md) for scope and contribution guidance.
