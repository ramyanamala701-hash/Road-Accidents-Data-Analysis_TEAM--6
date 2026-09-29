from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "outputs" / "figures"
REPORTS_DIR = ROOT / "reports"


def ensure_project_directories() -> None:
    for directory in (RAW_DIR, PROCESSED_DIR, FIGURES_DIR, REPORTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def first_existing(columns, aliases):
    """Find a source column case-insensitively after normalizing punctuation."""
    def normalize(value):
        return "".join(ch.lower() for ch in str(value) if ch.isalnum())

    lookup = {normalize(column): column for column in columns}
    for alias in aliases:
        match = lookup.get(normalize(alias))
        if match is not None:
            return match
    return None


def standardize_column_names(columns):
    """Return stable snake_case labels while avoiding name collisions."""
    used = set()
    standardized = []
    for original in columns:
        base = re.sub(r"[^0-9A-Za-z]+", "_", str(original).strip()).strip("_").lower()
        base = base or "unnamed_column"
        candidate = base
        suffix = 2
        while candidate in used:
            candidate = f"{base}_{suffix}"
            suffix += 1
        used.add(candidate)
        standardized.append(candidate)
    return standardized
