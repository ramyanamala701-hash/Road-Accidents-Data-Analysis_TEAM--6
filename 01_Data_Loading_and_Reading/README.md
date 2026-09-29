# Stage 1 — Data Loading & Reading

- **Purpose:** Inspect the supplied accident-level CSV before transformation.
- **Input:** `data/raw/india_road_accidents_dataset.csv` (240 rows × 25 fields in the provided file).
- **Processing:** Load the real CSV, display dimensions, column names, preview rows, dtypes, `info()`, and basic descriptive statistics. Confirm the required schema and accident ID granularity.
- **Output:** In-memory source frame and inspection in [01_data_loading_and_reading.ipynb](01_data_loading_and_reading.ipynb). The raw file is not modified.
- **Implementation:** `src/data_loader.py`.
