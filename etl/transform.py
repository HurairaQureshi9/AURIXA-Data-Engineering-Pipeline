from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DIR = PROJECT_ROOT / "DATA" / "cleaned"

# Load cleaned datasets
datasets = {
    file_path.stem.replace("_cleaned", ""): pd.read_csv(file_path)
    for file_path in CLEANED_DIR.glob("*.csv")
}

# Inspect schema and data quality
for name, df in datasets.items():
    print(f"\n{'=' * 50}")
    print(f"Dataset: {name}")
    print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nData types:")
    print(df.dtypes.to_string())
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"Missing values: {df.isna().sum().sum()}")

print(f"\nTotal datasets inspected: {len(datasets)}")