"""Audit this repository against its accident-level source and generated outputs."""
import csv
from datetime import datetime
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data/raw/india_road_accidents_dataset.csv"
EXPECTED = [
    "accident_id", "date_time", "year", "month", "state_ut", "district",
    "road_type", "weather", "road_surface", "lighting", "vehicle_type",
    "driver_age_group", "driver_gender", "speed_limit_kmph",
    "estimated_speed_kmph", "alcohol_involved", "helmet_seatbelt_used",
    "severity", "fatalities", "severe_injuries", "minor_injuries",
    "primary_cause", "pedestrians_involved", "latitude", "longitude",
]
STAGE_DIRS = [
    "01_Data_Loading_and_Reading", "02_Data_Acquisition_and_Filtering",
    "03_Data_Extraction", "04_Data_Validation_and_Cleaning",
    "05_Data_Aggregation_and_Representation", "06_Data_Analysis",
    "07_Data_Visualization", "08_Results_and_Interpretation",
]
AGGREGATES = [
    "accidents_by_year.csv", "accidents_by_month.csv", "accidents_by_state_ut.csv",
    "accidents_by_district.csv", "accidents_by_severity.csv", "fatalities_by_state_ut.csv",
    "injuries_by_state_ut.csv", "accidents_by_road_type.csv", "accidents_by_weather.csv",
    "accidents_by_road_surface.csv", "accidents_by_lighting.csv", "accidents_by_vehicle_type.csv",
    "accidents_by_driver_age_group.csv", "accidents_by_driver_gender.csv",
    "accidents_by_primary_cause.csv", "accidents_by_alcohol_involvement.csv",
    "accidents_by_helmet_seatbelt_usage.csv", "accidents_by_pedestrian_involvement.csv",
    "fatal_outcomes_by_primary_cause.csv",
]
SEVERITIES = {"Fatal", "Grievous Injury", "Minor Injury", "Property Damage Only"}
MONTHS = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}
BOOLS = {"true", "false", "1", "0", "yes", "no"}


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> int:
    checks = []

    def add(name, ok, detail="", critical=False):
        checks.append((name, bool(ok), str(detail), critical))

    rows, columns, load_error = [], [], ""
    try:
        with RAW.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            columns = reader.fieldnames or []
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        load_error = str(exc)
    add("raw CSV exists", RAW.is_file(), RAW.relative_to(ROOT), True)
    add("raw CSV can be loaded", not load_error, load_error or f"{len(rows)} data rows", True)
    add("expected 25 columns present and ordered", columns == EXPECTED,
        f"found {len(columns)} columns; expected exact 25-field schema", True)
    add("non-empty reasonable row count", 0 < len(rows) <= 1_000_000, len(rows), True)
    ids = [row.get("accident_id", "").strip() for row in rows]
    empty_ids = sum(not value for value in ids)
    duplicate_ids = len(ids) - len(set(ids))
    add("accident_id values present", empty_ids == 0, f"{empty_ids} blank IDs", True)
    add("accident IDs are unique", duplicate_ids == 0, f"{duplicate_ids} duplicate IDs", True)
    duplicate_rows = len(rows) - len({tuple(row.get(col, "") for col in columns) for row in rows})
    missing_by_column = {col: sum(not (row.get(col) or "").strip() for row in rows) for col in columns}
    missing_total = sum(missing_by_column.values())
    add("missing values reported", True, f"{missing_total} total; " + ", ".join(f"{k}={v}" for k, v in missing_by_column.items() if v) if missing_total else "0 across all columns")
    add("duplicate rows checked", duplicate_rows == 0, duplicate_rows, True)

    invalid = {"date_time": 0, "year": 0, "month": 0, "year_date_mismatch": 0,
               "month_date_mismatch": 0, "numeric_parse": 0, "negative_outcomes": 0,
               "speed_limit": 0, "estimated_speed": 0, "coordinates": 0,
               "boolean": 0, "severity": 0}
    for row in rows:
        parsed = None
        try:
            parsed = datetime.fromisoformat(row["date_time"].strip().replace("Z", "+00:00"))
        except (KeyError, ValueError, AttributeError):
            invalid["date_time"] += 1
        year = number(row.get("year"))
        if year is None or not year.is_integer() or not 1900 <= year <= 2100:
            invalid["year"] += 1
        elif parsed and int(year) != parsed.year:
            invalid["year_date_mismatch"] += 1
        month = row.get("month", "").strip()
        if month not in MONTHS:
            invalid["month"] += 1
        elif parsed and month != parsed.strftime("%b"):
            invalid["month_date_mismatch"] += 1
        for field in ("speed_limit_kmph", "estimated_speed_kmph", "fatalities", "severe_injuries", "minor_injuries", "latitude", "longitude"):
            if number(row.get(field)) is None:
                invalid["numeric_parse"] += 1
        for field in ("fatalities", "severe_injuries", "minor_injuries"):
            value = number(row.get(field))
            if value is not None and value < 0:
                invalid["negative_outcomes"] += 1
        value = number(row.get("speed_limit_kmph"))
        if value is None or value <= 0 or value > 180:
            invalid["speed_limit"] += 1
        value = number(row.get("estimated_speed_kmph"))
        if value is None or value < 0 or value > 300:
            invalid["estimated_speed"] += 1
        lat, lon = number(row.get("latitude")), number(row.get("longitude"))
        if lat is None or lon is None or not -90 <= lat <= 90 or not -180 <= lon <= 180:
            invalid["coordinates"] += 1
        if any(row.get(field, "").strip().casefold() not in BOOLS for field in
               ("alcohol_involved", "helmet_seatbelt_used", "pedestrians_involved")):
            invalid["boolean"] += 1
        if row.get("severity", "").strip() not in SEVERITIES:
            invalid["severity"] += 1
    invalid_total = sum(invalid.values())
    add("numeric/date/category validation", invalid_total == 0, invalid, True)
    add("negative fatalities/injuries checked", invalid["negative_outcomes"] == 0,
        invalid["negative_outcomes"], True)

    processed_paths = [ROOT / "data/processed/cleaned_accidents.csv",
                       ROOT / "data/processed/extracted_accidents.csv",
                       ROOT / "data/processed/pipeline_summary.json"]
    add("processed outputs exist", all(path.is_file() for path in processed_paths),
        f"{sum(path.is_file() for path in processed_paths)}/{len(processed_paths)}")
    aggregate_dir = ROOT / "data/processed/aggregates"
    missing_aggregates = [name for name in AGGREGATES if not (aggregate_dir / name).is_file()]
    add("required aggregate files exist", not missing_aggregates, f"{len(AGGREGATES)-len(missing_aggregates)}/{len(AGGREGATES)}")
    figures = [path for path in (ROOT / "outputs/figures").glob("*.svg") if path.is_file()]
    add("figures exist", len(figures) >= 4, f"{len(figures)} SVG charts")

    notebooks = sorted(ROOT.rglob("*.ipynb"))
    stage_notebooks = [ROOT / folder / (folder[:2] + "_" + folder[3:].lower() + ".ipynb") for folder in STAGE_DIRS]
    expected_names = ["01_data_loading_and_reading.ipynb", "02_data_acquisition_and_filtering.ipynb",
                      "03_data_extraction.ipynb", "04_data_validation_and_cleaning.ipynb",
                      "05_data_aggregation_and_representation.ipynb", "06_data_analysis.ipynb",
                      "07_data_visualization.ipynb", "08_results_and_interpretation.ipynb"]
    stage_notebooks = [ROOT / folder / name for folder, name in zip(STAGE_DIRS, expected_names)]
    add("all eight stage notebooks exist", all(path.is_file() for path in stage_notebooks),
        f"{sum(path.is_file() for path in stage_notebooks)}/8")
    add("all eight stage READMEs exist", all((ROOT / folder / "README.md").is_file() for folder in STAGE_DIRS),
        f"{sum((ROOT / folder / 'README.md').is_file() for folder in STAGE_DIRS)}/8")
    hashes = {}
    for path in notebooks:
        hashes.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), []).append(path)
    duplicates = [group for group in hashes.values() if len(group) > 1]
    add("no duplicate notebooks", not duplicates, f"{len(notebooks)} notebooks scanned")
    for rel in ["PROJECT_SPEC.md", "reports/DATA_DICTIONARY.md", "requirements.txt", "README.md"]:
        add(f"{rel} exists", (ROOT / rel).is_file(), critical=rel == "PROJECT_SPEC.md")
    modules = list((ROOT / "src").glob("*.py"))
    add("source modules exist", bool(modules), f"{len(modules)} modules")
    add("no .pyc files", not list(ROOT.rglob("*.pyc")))
    add("no __pycache__ directories", not [path for path in ROOT.rglob("__pycache__") if path.is_dir()])

    old_raw_name = "road_accidents_india_state_ut_" + "2016_2019.csv"
    add("old raw CSV is not active", not (ROOT / "data/raw" / old_raw_name).exists())
    banned = [old_raw_name, "Road_Accidents_" + "2016", "Road_Accidents_" + "2017",
              "Road_Accidents_" + "2018", "Road_Accidents_" + "2019"]
    stale = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".ipynb", ".json", ".csv", ".svg"}:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if any(token in text for token in banned):
                stale.append(str(path.relative_to(ROOT)))
    add("no stale previous-schema references", not stale, ", ".join(stale) or "none found")

    print("India Road Accident Analytics - accident-level project audit")
    for name, ok, detail, _ in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}".rstrip())
    failures = [name for name, ok, _, critical in checks if critical and not ok]
    print(f"\n{sum(ok for _, ok, _, _ in checks)}/{len(checks)} checks passed.")
    if failures:
        print("Critical failures: " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
