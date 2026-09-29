# Stage 7 — Data Visualization

- **Purpose:** Show category frequencies and numeric comparisons clearly.
- **Input:** Cleaned records and their calculated aggregate tables.
- **Charts:** Year, State/UT, severity, primary cause, vehicle type, road type, weather, lighting, State/UT fatalities, month, alcohol involvement, pedestrian involvement, and estimated speed versus listed speed limit.
- **Output:** SVG figures in `outputs/figures/`, regenerated from the current CSV by the pipeline.
- **Implementation:** `src/visualization.py`; SVG creation does not require plotting packages.
- **Interpretation:** Charts visualize this file only. The speed equality line is a reference, not a fitted relationship.
