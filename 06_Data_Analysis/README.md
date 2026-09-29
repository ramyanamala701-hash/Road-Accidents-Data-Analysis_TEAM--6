# Stage 6 — Data Analysis

- **Purpose:** Answer descriptive questions using only observed records.
- **Questions:** Highest State/UT record/fatality counts; most frequent severity, cause, vehicle, and age group; annual/monthly patterns; weather, lighting, and road-type counts; alcohol/pedestrian flags; estimated speed compared with limit; and fatal outcomes grouped by recorded primary cause.
- **Output:** Dynamically calculated observations in `data/processed/pipeline_summary.json` and `reports/RESULTS_SUMMARY.md`.
- **Implementation:** `analyze_dataset` in `src/analysis.py`.
- **Interpretation:** Use “recorded,” “observed,” and “associated with.” These summaries do not establish causes or representativeness.
