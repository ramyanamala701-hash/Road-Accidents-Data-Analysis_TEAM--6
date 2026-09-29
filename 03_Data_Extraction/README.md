# Stage 3 — Data Extraction

- **Purpose:** Map existing source fields into thematic groups and derive compact calendar features.
- **Input:** The 25 actual fields from the user-provided CSV.
- **Processing:** Inspect the timestamp, location, road conditions, driver/vehicle, speed, safety, outcome, and cause field groups. Derive accident date, hour, and month number from the recorded timestamp.
- **Output:** `data/processed/extracted_accidents.csv`, keyed by accident ID; this compact table avoids duplicating all source fields.
- **Implementation:** `COLUMN_GROUPS` and `extract_analysis_fields` in `src/data_extraction.py`.
