"""Explicit, optional filters for accident-level records."""
import pandas as pd


def _boolean_series(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    return series.astype("string").str.strip().str.casefold().map(
        {"true": True, "1": True, "yes": True, "false": False, "0": False, "no": False}
    ).fillna(False)


def _match(series: pd.Series, values) -> pd.Series:
    wanted = {str(v).strip().casefold() for v in values}
    return series.astype("string").str.strip().str.casefold().isin(wanted)


def filter_records(df: pd.DataFrame, years=None, locations=None, severities=None,
                   fatal_only=False, pedestrians=None, alcohol=None,
                   road_types=None, weather=None) -> pd.DataFrame:
    """Filter only when requested; default returns all supplied records."""
    result = df.copy()
    filters = [(years, "year"), (locations, "state_ut"), (severities, "severity"),
               (road_types, "road_type"), (weather, "weather")]
    for values, column in filters:
        if values is None:
            continue
        if column not in result:
            raise ValueError(f"Cannot filter by {column}: column is absent.")
        if column == "year":
            result = result.loc[pd.to_numeric(result[column], errors="coerce").isin(list(values))]
        else:
            result = result.loc[_match(result[column], values)]
    if fatal_only:
        if "fatalities" not in result:
            raise ValueError("Cannot select fatal accidents: fatalities column is absent.")
        result = result.loc[pd.to_numeric(result.fatalities, errors="coerce").gt(0)]
    for requested, column in ((pedestrians, "pedestrians_involved"), (alcohol, "alcohol_involved")):
        if requested is not None:
            if column not in result:
                raise ValueError(f"Cannot filter by {column}: column is absent.")
            result = result.loc[_boolean_series(result[column]).eq(bool(requested))]
    return result.copy()
