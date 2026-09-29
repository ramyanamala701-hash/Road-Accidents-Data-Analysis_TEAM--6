# Contributing

1. Use Python 3.10 or newer and install dependencies with `python -m pip install -r requirements.txt`.
2. Keep the user-provided CSV at `data/raw/india_road_accidents_dataset.csv`; treat the raw file as read-only.
3. Run all stages with `python run_pipeline.py` or `python -m src.run_pipeline` from the project root.
4. Run `python audit_pipeline_outputs.py` to check the schema, data quality, outputs, notebooks, and repository consistency.
5. Put transformations in `src/` and stage explanations in the corresponding numbered notebook/README. Use only fields present in the actual CSV or explicitly documented derived measures.
6. Do not impute values without a documented reason, invent records, infer causation from descriptive patterns, or claim the file is nationally representative.
7. Re-run the pipeline and review generated outputs after changing processing logic. Keep notebooks in the eight numbered stage folders; do not add duplicate notebooks or generated caches.
