# Stage 2 — Data Acquisition & Filtering

- **Purpose:** Show transparent subsets from the supplied records while retaining all rows in the default pipeline.
- **Input:** The raw accident-level CSV.
- **Processing:** Demonstrate filters for year, State/UT, severity, fatalities, pedestrian involvement, alcohol involvement, road type, and weather using observed values.
- **Output:** In-memory filter examples; the pipeline does not write a redundant full-table acquired copy.
- **Implementation:** `src/data_acquisition.py`.
- **Interpretation:** Each subset describes this file only and does not imply representativeness or causation.
