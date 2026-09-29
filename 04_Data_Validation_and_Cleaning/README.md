# Stage 4 — Data Validation & Cleaning

- **Purpose:** Report data quality and save a conservative typed copy.
- **Input:** Accident-level source fields (Stage 3's compact feature table is not used to replace the source fields).
- **Checks:** Missing values, exact duplicate rows, duplicate accident IDs, date parsing, year/month and timestamp consistency, numeric ranges, nonnegative injury/fatality counts, speed, coordinates, Boolean values, gender, and severity.
- **Handling:** Invalid typed/domain values become missing in the processed copy and are counted. No values are imputed. Exact duplicate rows are removed from the copy; duplicate IDs are reported and retained. The raw file stays unchanged.
- **Output:** `data/processed/cleaned_accidents.csv` and quality details in the pipeline summary.
- **Implementation:** `src/data_cleaning.py`.
