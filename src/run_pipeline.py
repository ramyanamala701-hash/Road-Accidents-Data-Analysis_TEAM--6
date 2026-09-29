"""Run all eight stages for the provided accident-level dataset."""
import json
from pathlib import Path
import pandas as pd

from .data_loader import EXPECTED_COLUMNS, find_dataset, load_dataset, inspect_dataset
from .data_acquisition import filter_records
from .data_extraction import extract_analysis_fields, normalize_source
from .data_cleaning import clean_dataset
from .analysis import analyze_dataset, save_aggregations
from .visualization import create_visualizations
from .utils import PROCESSED_DIR, REPORTS_DIR, ensure_project_directories


def _table_markdown(frame: pd.DataFrame, columns=None, limit=15) -> str:
    if frame is None or frame.empty:
        return "No rows available."
    view = frame.loc[:, columns] if columns else frame
    view = view.head(limit)
    lines = ["| " + " | ".join(view.columns.astype(str)) + " |",
             "| " + " | ".join("---" for _ in view.columns) + " |"]
    for row in view.itertuples(index=False, name=None):
        vals = ["NA" if pd.isna(value) else (f"{value:,.1f}" if isinstance(value, float) else str(value)) for value in row]
        lines.append("| " + " | ".join(value.replace("|", "\\|") for value in vals) + " |")
    return "\n".join(lines)


def write_results_report(result: dict, tables: dict[str, pd.DataFrame]) -> Path:
    summary_tables = [
        ("Accidents by year", "accidents_by_year", ["year", "accident_count"]),
        ("Accidents by State/UT", "accidents_by_state_ut", ["state_ut", "accident_count"]),
        ("Fatalities by State/UT", "fatalities_by_state_ut", ["state_ut", "fatalities"]),
        ("Severity distribution", "accidents_by_severity", ["severity", "accident_count"]),
        ("Primary cause and recorded fatal outcomes", "fatal_outcomes_by_primary_cause", ["primary_cause", "accident_count", "fatal_accident_count", "fatalities"]),
    ]
    sections = []
    for title, key, columns in summary_tables:
        if key in tables:
            sections.append(f"## {title}\n\n{_table_markdown(tables[key], columns)}")
    findings = "\n".join(f"- {line}" for line in result["observations"])
    content = f'''# Results Summary

## Dataset and method

This report is computed from `{result['source_file']}`, the user-provided accident-level CSV. The loaded source had {result['source_rows']:,} rows and {result['source_columns']:,} columns. {result['filtered_rows']:,} records were included in this run; {result['cleaned_rows']:,} remain after exact duplicate-row handling. This dataset is not asserted to be a complete official or nationally representative record of Indian road accidents.

## Key findings observed in these records

{findings}

{chr(10).join(sections)}

## Data quality

```json
{json.dumps(result['quality'], indent=2, default=str)}
```

## Interpretation and limitations

Results describe counts and values recorded in this supplied dataset only. They do not establish that a road, weather condition, driver group, or behavior caused an accident. The source's collection method, sampling coverage, and representativeness are not established by the CSV alone. `helmet_seatbelt_used` combines two safety-device concepts in one field, so applicability can differ by vehicle. Coordinates are summarized as supplied and are not independently verified.

## Reproducibility

From the project root, run `python -m src.run_pipeline` or `python run_pipeline.py`. The raw source is read only; processed files, aggregate tables, figures, and this report are regenerated from it.
'''
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / "RESULTS_SUMMARY.md"
    path.write_text(content, encoding="utf-8")
    return path


def run_pipeline(dataset_path=None, years=None, locations=None, severities=None,
                 fatal_only=False, pedestrians=None, alcohol=None,
                 road_types=None, weather=None):
    ensure_project_directories()
    source_path = find_dataset(dataset_path)
    raw = load_dataset(source_path)
    initial = inspect_dataset(raw)
    normalized = normalize_source(raw)
    acquired = filter_records(normalized, years=years, locations=locations,
                              severities=severities, fatal_only=fatal_only,
                              pedestrians=pedestrians, alcohol=alcohol,
                              road_types=road_types, weather=weather)
    extracted, column_groups = extract_analysis_fields(acquired)
    extracted_path = PROCESSED_DIR / "extracted_accidents.csv"
    extracted.to_csv(extracted_path, index=False)
    cleaned, quality = clean_dataset(acquired)
    cleaned_path = PROCESSED_DIR / "cleaned_accidents.csv"
    cleaned.to_csv(cleaned_path, index=False)
    tables, observations = analyze_dataset(cleaned)
    aggregate_paths = save_aggregations(tables, PROCESSED_DIR / "aggregates")
    figures = create_visualizations(cleaned)
    result = {
        "source_file": source_path.name,
        "source_rows": initial["rows"],
        "source_columns": initial["columns"],
        "source_column_names": initial["column_names"],
        "filtered_rows": int(len(acquired)),
        "cleaned_rows": int(len(cleaned)),
        "column_groups": column_groups,
        "quality": quality,
        "processed_files": [str(extracted_path.relative_to(Path(__file__).resolve().parents[1])),
                            str(cleaned_path.relative_to(Path(__file__).resolve().parents[1]))],
        "aggregation_files": [str(p.relative_to(Path(__file__).resolve().parents[1])) for p in aggregate_paths],
        "figures": [str(p.relative_to(Path(__file__).resolve().parents[1])) for p in figures],
        "observations": observations,
    }
    write_results_report(result, tables)
    (PROCESSED_DIR / "pipeline_summary.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    # Remove a no-longer-used full-table copy produced by the previous workflow.
    (PROCESSED_DIR / "acquired_accidents.csv").unlink(missing_ok=True)
    return result


if __name__ == "__main__":
    try:
        summary = run_pipeline()
    except (FileNotFoundError, ValueError, ImportError) as error:
        raise SystemExit(str(error)) from None
    print(f"Pipeline complete: {summary['cleaned_rows']} accident records processed; "
          f"{len(summary['aggregation_files'])} aggregate tables and {len(summary['figures'])} figures generated.")
