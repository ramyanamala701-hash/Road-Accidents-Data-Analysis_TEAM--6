"""Validate and conservatively clean the supplied accident-level records."""
import pandas as pd

from .data_extraction import normalize_source

SEVERITIES = {"Fatal", "Grievous Injury", "Minor Injury", "Property Damage Only"}
MONTHS = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}
GENDERS = {"Male", "Female"}
BOOLEAN_COLUMNS = ["alcohol_involved", "helmet_seatbelt_used", "pedestrians_involved"]
COUNT_COLUMNS = ["fatalities", "severe_injuries", "minor_injuries"]


def quality_report(df: pd.DataFrame) -> dict:
    result = {"rows": int(len(df)), "columns": int(df.shape[1]),
              "missing_cells": int(df.isna().sum().sum()),
              "missing_by_column": {str(k): int(v) for k, v in df.isna().sum().items()},
              "duplicate_rows": int(df.duplicated().sum()),
              "duplicate_accident_ids": int(df["accident_id"].duplicated(keep=False).sum())
              if "accident_id" in df else None}
    invalid = {}
    if "date_time" in df:
        parsed = pd.to_datetime(df.date_time, errors="coerce")
        invalid["date_time"] = int(parsed.isna().sum())
        if "year" in df:
            years = pd.to_numeric(df.year, errors="coerce")
            invalid["year"] = int((years.isna() | years.lt(1900) | years.gt(2100)).sum())
            invalid["year_date_mismatch"] = int((parsed.notna() & years.notna() & years.ne(parsed.dt.year)).sum())
        if "month" in df:
            invalid["month"] = int((~df.month.isin(MONTHS)).sum())
            invalid["month_date_mismatch"] = int((parsed.notna() & df.month.isin(MONTHS) & df.month.ne(parsed.dt.strftime("%b"))).sum())
    numeric_rules = {
        "speed_limit_kmph": lambda s: s.isna() | s.le(0) | s.gt(180),
        "estimated_speed_kmph": lambda s: s.isna() | s.lt(0) | s.gt(300),
        "fatalities": lambda s: s.isna() | s.lt(0),
        "severe_injuries": lambda s: s.isna() | s.lt(0),
        "minor_injuries": lambda s: s.isna() | s.lt(0),
        "latitude": lambda s: s.isna() | s.lt(-90) | s.gt(90),
        "longitude": lambda s: s.isna() | s.lt(-180) | s.gt(180),
    }
    for column, rule in numeric_rules.items():
        if column in df:
            invalid[column] = int(rule(pd.to_numeric(df[column], errors="coerce")).sum())
    if "severity" in df:
        invalid["severity"] = int((~df.severity.isin(SEVERITIES)).sum())
    if "driver_gender" in df:
        invalid["driver_gender"] = int((~df.driver_gender.isin(GENDERS)).sum())
    for column in BOOLEAN_COLUMNS:
        if column in df:
            normalized = df[column].astype("string").str.strip().str.casefold()
            invalid[column] = int((~normalized.isin({"true", "false", "1", "0", "yes", "no"})).sum())
    result["invalid_values"] = invalid
    return result


def _parse_boolean(series: pd.Series) -> pd.Series:
    normalized = series.astype("string").str.strip().str.casefold()
    return normalized.map({"true": True, "1": True, "yes": True,
                           "false": False, "0": False, "no": False}).astype("boolean")


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    source = normalize_source(df)
    before = quality_report(source)
    result = source.copy()
    for column in result.select_dtypes(include=["object", "string"]).columns:
        result[column] = result[column].astype("string").str.strip().replace("", pd.NA)
    result["date_time"] = pd.to_datetime(result.date_time, errors="coerce")
    numeric = ["year", "speed_limit_kmph", "estimated_speed_kmph", *COUNT_COLUMNS, "latitude", "longitude"]
    for column in numeric:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    result["year"] = result.year.astype("Int64")
    result.loc[~result.year.between(1900, 2100), "year"] = pd.NA
    result.loc[~result.speed_limit_kmph.between(1, 180), "speed_limit_kmph"] = pd.NA
    result.loc[~result.estimated_speed_kmph.between(0, 300), "estimated_speed_kmph"] = pd.NA
    for column in COUNT_COLUMNS:
        result.loc[result[column].lt(0), column] = pd.NA
    result.loc[~result.latitude.between(-90, 90), "latitude"] = pd.NA
    result.loc[~result.longitude.between(-180, 180), "longitude"] = pd.NA
    result.loc[~result.month.isin(MONTHS), "month"] = pd.NA
    result.loc[~result.severity.isin(SEVERITIES), "severity"] = pd.NA
    result.loc[~result.driver_gender.isin(GENDERS), "driver_gender"] = pd.NA
    for column in BOOLEAN_COLUMNS:
        result[column] = _parse_boolean(result[column])
    duplicate_rows = int(result.duplicated().sum())
    result = result.drop_duplicates().copy()
    after = quality_report(result)
    after["exact_duplicate_rows_removed"] = duplicate_rows
    return result, {"before": before, "after": after,
                    "handling": "Invalid typed/domain values become missing in the processed copy and are counted; no values are imputed. Exact duplicate rows are removed from the processed copy. Duplicate IDs are reported, not silently discarded. The raw source is never changed."}
