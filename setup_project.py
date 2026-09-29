"""Read-only environment and project readiness check; makes no changes."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "data/raw/india_road_accidents_dataset.csv",
    "src/run_pipeline.py",
    "requirements.txt",
]


def main() -> int:
    print(f"Python: {sys.version.split()[0]} ({'OK' if sys.version_info >= (3, 10) else 'requires 3.10+'})")
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    for name in REQUIRED:
        print(f"{'OK' if name not in missing else 'MISSING'}: {name}")
    dependency_ok = True
    try:
        import pandas  # noqa: F401
    except ImportError:
        dependency_ok = False
        print("MISSING dependency: pandas. Install dependencies with: python -m pip install -r requirements.txt")
    else:
        print("OK: pandas")
    return 1 if sys.version_info < (3, 10) or missing or not dependency_ok else 0


if __name__ == "__main__":
    raise SystemExit(main())
