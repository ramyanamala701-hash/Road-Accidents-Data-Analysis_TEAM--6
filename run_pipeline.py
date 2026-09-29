"""Convenience launcher for the existing eight-stage pipeline."""
from src.run_pipeline import run_pipeline


if __name__ == "__main__":
    result = run_pipeline()
    print(f"Pipeline completed: {result['source_rows']} source rows; "
          f"{result['cleaned_rows']} processed rows.")
