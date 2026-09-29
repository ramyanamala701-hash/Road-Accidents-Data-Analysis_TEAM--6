# Stage 5 — Data Aggregation & Representation

- **Purpose:** Create interpretable tables from the cleaned accident records.
- **Input:** `data/processed/cleaned_accidents.csv`.
- **Processing:** Aggregate recorded accident counts, fatalities, injury counts, and selected Boolean indicators by year/month, State/UT/district, severity, road/environment, vehicle/driver, cause, and safety flags.
- **Outputs:** 19 named CSV tables in `data/processed/aggregates/`, including dedicated State/UT fatalities and injury summaries and fatal outcomes by primary-cause label.
- **Implementation:** `src/data_aggregation.py` and `src/analysis.py`.
- **Interpretation:** Summaries count records in the provided file; they are not exposure-adjusted rates.
