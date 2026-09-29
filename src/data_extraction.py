"""Extract a compact calendar/location feature table and map source fields."""
import pandas as pd

from .data_loader import EXPECTED_COLUMNS
from .utils import standardize_column_names

COLUMN_GROUPS = {
    "date_time": ["date_time", "year", "month"],
    "location": ["state_ut", "district", "latitude", "longitude"],
    "road_conditions": ["road_type", "weather", "road_surface", "lighting"],
    "driver_vehicle": ["vehicle_type", "driver_age_group", "driver_gender"],
    "speed": ["speed_limit_kmph", "estimated_speed_kmph"],
    "safety": ["alcohol_involved", "helmet_seatbelt_used", "pedestrians_involved"],
    "severity_injuries": ["severity", "fatalities", "severe_injuries", "minor_injuries"],
    "cause": ["primary_cause"],
}


def normalize_source(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.columns = standardize_column_names(result.columns)
    missing = [column for column in EXPECTED_COLUMNS if column not in result.columns]
    if missing:
        raise ValueError(f"The accident dataset is missing required columns: {missing}")
    return result.loc[:, EXPECTED_COLUMNS].copy()


def extract_analysis_fields(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Produce compact derived calendar fields, not a second copy of all data."""
    source = normalize_source(df)
    stamp = pd.to_datetime(source["date_time"], errors="coerce")
    extracted = pd.DataFrame({
        "accident_id": source["accident_id"],
        "accident_date": stamp.dt.strftime("%Y-%m-%d"),
        "accident_hour": stamp.dt.hour.astype("Int64"),
        "year": pd.to_numeric(source["year"], errors="coerce").astype("Int64"),
        "month": source["month"],
        "month_number": stamp.dt.month.astype("Int64"),
    })
    mapping = {group: [column for column in columns if column in source.columns]
               for group, columns in COLUMN_GROUPS.items()}
    return extracted, mapping
