"""Build descriptive aggregates from accident-level records."""
from pathlib import Path
import pandas as pd

GROUPS = {
    "year": "accidents_by_year",
    "month": "accidents_by_month",
    "state_ut": "accidents_by_state_ut",
    "district": "accidents_by_district",
    "severity": "accidents_by_severity",
    "road_type": "accidents_by_road_type",
    "weather": "accidents_by_weather",
    "road_surface": "accidents_by_road_surface",
    "lighting": "accidents_by_lighting",
    "vehicle_type": "accidents_by_vehicle_type",
    "driver_age_group": "accidents_by_driver_age_group",
    "driver_gender": "accidents_by_driver_gender",
    "primary_cause": "accidents_by_primary_cause",
    "alcohol_involved": "accidents_by_alcohol_involvement",
    "helmet_seatbelt_used": "accidents_by_helmet_seatbelt_usage",
    "pedestrians_involved": "accidents_by_pedestrian_involvement",
}
MONTH_ORDER = {name: index for index, name in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in ["fatalities", "severe_injuries", "minor_injuries", "speed_limit_kmph", "estimated_speed_kmph"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result["nonfatal_injuries"] = result["severe_injuries"].fillna(0) + result["minor_injuries"].fillna(0)
    result["above_speed_limit"] = result["estimated_speed_kmph"].gt(result["speed_limit_kmph"])
    result["alcohol_count"] = result["alcohol_involved"].astype("boolean").fillna(False).astype(int)
    result["pedestrian_count"] = result["pedestrians_involved"].astype("boolean").fillna(False).astype(int)
    result["over_limit_count"] = result["above_speed_limit"].fillna(False).astype(int)
    return result


def _group(df: pd.DataFrame, category: str) -> pd.DataFrame:
    data = _prepare(df)
    table = data.groupby(category, dropna=False).agg(
        accident_count=("accident_id", "size"),
        fatalities=("fatalities", "sum"),
        severe_injuries=("severe_injuries", "sum"),
        minor_injuries=("minor_injuries", "sum"),
        nonfatal_injuries=("nonfatal_injuries", "sum"),
        alcohol_involved_accidents=("alcohol_count", "sum"),
        pedestrian_involved_accidents=("pedestrian_count", "sum"),
        above_speed_limit_records=("over_limit_count", "sum"),
    ).reset_index()
    if category == "month":
        table["_order"] = table[category].map(MONTH_ORDER).fillna(99)
        table = table.sort_values(["_order", category]).drop(columns="_order")
    elif category == "year":
        table = table.sort_values(category)
    else:
        table = table.sort_values("accident_count", ascending=False, kind="stable")
    return table.reset_index(drop=True)


def build_aggregations(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    tables = {filename: _group(df, column) for column, filename in GROUPS.items()}
    state = _prepare(df).groupby("state_ut", dropna=False)
    tables["fatalities_by_state_ut"] = state["fatalities"].sum().reset_index().sort_values("fatalities", ascending=False).reset_index(drop=True)
    injuries = _prepare(df).groupby("state_ut", dropna=False)[["severe_injuries", "minor_injuries", "nonfatal_injuries"]].sum().reset_index()
    tables["injuries_by_state_ut"] = injuries.sort_values("nonfatal_injuries", ascending=False).reset_index(drop=True)
    cause = _prepare(df).assign(fatal_accident=lambda d: d.fatalities.gt(0)).groupby("primary_cause", dropna=False).agg(
        accident_count=("accident_id", "size"),
        fatal_accident_count=("fatal_accident", "sum"),
        fatalities=("fatalities", "sum"),
    ).reset_index().sort_values("fatalities", ascending=False).reset_index(drop=True)
    tables["fatal_outcomes_by_primary_cause"] = cause
    return tables


def save_aggregations(tables: dict[str, pd.DataFrame], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    # Remove stale summary CSVs so the directory always represents this run.
    for old in output_dir.glob("*.csv"):
        old.unlink()
    paths = []
    for filename, table in tables.items():
        path = output_dir / f"{filename}.csv"
        table.to_csv(path, index=False)
        paths.append(path)
    return paths
