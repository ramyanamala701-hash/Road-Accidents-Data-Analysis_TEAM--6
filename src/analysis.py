"""Descriptive findings for the supplied accident-level records."""
from pathlib import Path
import pandas as pd

from .data_aggregation import build_aggregations


def _top(table: pd.DataFrame, category: str, metric: str) -> tuple[str, float] | None:
    eligible = table.dropna(subset=[metric])
    if eligible.empty:
        return None
    row = eligible.sort_values(metric, ascending=False, kind="stable").iloc[0]
    return str(row[category]), float(row[metric])


def analyze_dataset(df: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], list[str]]:
    tables = build_aggregations(df)
    observations = []
    for table_name, category, metric, phrase in [
        ("accidents_by_state_ut", "state_ut", "accident_count", "most recorded accidents by State/UT"),
        ("fatalities_by_state_ut", "state_ut", "fatalities", "highest recorded fatalities by State/UT"),
        ("accidents_by_severity", "severity", "accident_count", "most frequent recorded severity"),
        ("accidents_by_primary_cause", "primary_cause", "accident_count", "most frequently recorded primary cause"),
        ("accidents_by_vehicle_type", "vehicle_type", "accident_count", "most frequently recorded vehicle type"),
        ("accidents_by_weather", "weather", "accident_count", "highest recorded weather category count"),
        ("accidents_by_lighting", "lighting", "accident_count", "highest recorded lighting category count"),
        ("accidents_by_road_type", "road_type", "accident_count", "highest recorded road type count"),
        ("accidents_by_driver_age_group", "driver_age_group", "accident_count", "most frequent recorded driver age group"),
    ]:
        result = _top(tables[table_name], category, metric)
        if result:
            observations.append(f"{result[0]} has the {phrase} ({result[1]:,.0f} records in this dataset).")
    years = tables["accidents_by_year"]
    if not years.empty:
        observations.append("Accident records by year: " + "; ".join(
            f"{int(row.year)}: {int(row.accident_count):,}" for row in years.itertuples()))
    months = tables["accidents_by_month"]
    if not months.empty:
        result = _top(months, "month", "accident_count")
        observations.append(f"{result[0]} has the highest recorded month count ({result[1]:,.0f}).")
    for column, label in [("alcohol_involved", "alcohol-involved"), ("pedestrians_involved", "pedestrian-involved")]:
        count = int(df[column].astype("boolean").fillna(False).sum())
        pct = count / len(df) * 100 if len(df) else 0
        observations.append(f"{count:,} of {len(df):,} records ({pct:.1f}%) are marked {label}.")
    limit = pd.to_numeric(df.speed_limit_kmph, errors="coerce")
    speed = pd.to_numeric(df.estimated_speed_kmph, errors="coerce")
    valid = limit.notna() & speed.notna()
    above = int((speed[valid] > limit[valid]).sum())
    count = int(valid.sum())
    mean_delta = float((speed[valid] - limit[valid]).mean()) if count else float("nan")
    observations.append(f"Estimated speed exceeds the listed speed limit in {above:,} of {count:,} records with both values ({above / count * 100:.1f}%); mean estimated-minus-limit difference is {mean_delta:.1f} km/h." if count else "No complete speed-limit and estimated-speed pairs are available.")
    fatal_causes = tables["fatal_outcomes_by_primary_cause"]
    fatal_causes = fatal_causes.loc[fatal_causes.fatalities.gt(0)]
    if not fatal_causes.empty:
        top = fatal_causes.iloc[0]
        observations.append(f"{top.primary_cause} has the highest recorded fatality total by primary cause ({int(top.fatalities):,} fatalities); this is an observed association, not evidence of causation.")
    return tables, observations


def save_aggregations(tables: dict[str, pd.DataFrame], output_dir: Path) -> list[Path]:
    from .data_aggregation import save_aggregations as save
    return save(tables, output_dir)
