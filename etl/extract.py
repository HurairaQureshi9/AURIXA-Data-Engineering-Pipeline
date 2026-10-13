from pathlib import Path
import pandas as pd

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DIR = PROJECT_ROOT / "DATA" / "cleaned"

# Extract cleaned CSV files
datasets = {}

for file_path in CLEANED_DIR.glob("*.csv"):
    dataset_name = file_path.stem.replace("_cleaned", "")
    datasets[dataset_name] = pd.read_csv(file_path)
    print(f"{dataset_name}: {datasets[dataset_name].shape}")

print(f"\nTotal datasets extracted: {len(datasets)}")