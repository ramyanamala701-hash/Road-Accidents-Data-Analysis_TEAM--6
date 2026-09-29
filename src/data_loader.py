"""Load the project's actual accident-level CSV source."""
from pathlib import Path
import os
import pandas as pd

from .utils import RAW_DIR

DATASET_FILENAME = "india_road_accidents_dataset.csv"
EXPECTED_COLUMNS = [
    "accident_id", "date_time", "year", "month", "state_ut", "district",
    "road_type", "weather", "road_surface", "lighting", "vehicle_type",
    "driver_age_group", "driver_gender", "speed_limit_kmph",
    "estimated_speed_kmph", "alcohol_involved", "helmet_seatbelt_used",
    "severity", "fatalities", "severe_injuries", "minor_injuries",
    "primary_cause", "pedestrians_involved", "latitude", "longitude",
]


def find_dataset(path=None) -> Path:
    """Return the canonical file, an explicit path, or ACCIDENT_DATA_FILE."""
    configured = path or os.getenv("ACCIDENT_DATA_FILE") or DATASET_FILENAME
    candidate = Path(configured)
    if not candidate.is_absolute():
        candidate = RAW_DIR / candidate
    if not candidate.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {candidate}. Place the supplied accident-level CSV at "
            f"data/raw/{DATASET_FILENAME} and install dependencies with "
            "`python -m pip install -r requirements.txt`."
        )
    if candidate.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV dataset, received: {candidate.suffix}")
    return candidate


def load_dataset(path=None, **read_options) -> pd.DataFrame:
    return pd.read_csv(find_dataset(path), **read_options)


def inspect_dataset(df: pd.DataFrame) -> dict:
    print("First rows:\n", df.head(), "\n", sep="")
    print(f"Shape: {df.shape}")
    print("Columns:", df.columns.tolist())
    print("\nData types:\n", df.dtypes.to_string())
    print("\nDataFrame info:")
    df.info()
    print("\nDescriptive statistics:\n", df.describe(include="all").transpose())
    return {"rows": int(df.shape[0]), "columns": int(df.shape[1]), "column_names": df.columns.tolist()}
