# Stage 8 — Results & Interpretation

- **Purpose:** Present calculated patterns, data quality, interpretation limits, and conclusion.
- **Input:** The supplied accident-level CSV and outputs from Stages 1–7.
- **Processing:** Run the complete pipeline; key findings and summary tables are rebuilt from the actual source values.
- **Output:** `reports/RESULTS_SUMMARY.md`, `data/processed/pipeline_summary.json`, aggregate CSVs, and figures.
- **Implementation:** `run_pipeline` and `write_results_report` in `src/run_pipeline.py`.
- **Limit:** Findings describe records in this provided file. Recorded primary cause is not proof of causation, and file coverage is not established as nationally complete.
