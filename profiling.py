import pandas as pd
from pathlib import Path

# Raw data folder
raw_path = Path("data/raw")

# Reports folder
reports_path = Path("reports")
reports_path.mkdir(exist_ok=True)

# Find all CSV files automatically
files = list(raw_path.glob("*.csv"))

print("FILES FOUND:")
print(files)

# Store profiling summary
report_data = []

# Profile every CSV file
for file in files:
    df = pd.read_csv(file)

    print("\n" + "=" * 60)
    print("FILE:", file.name)

    print("\nSHAPE:")
    print(df.shape)

    print("\nCOLUMNS:")
    print(df.columns.tolist())

    print("\nMISSING VALUES:")
    print(df.isna().sum())

    print("\nDUPLICATES:")
    print(df.duplicated().sum())

    print("\nDUPLICATE ROWS:")
    print(df[df.duplicated()].head())

    print("\nROWS AFTER REMOVING DUPLICATES:")
    print(df.drop_duplicates().shape)

    print("\nROWS AFTER REMOVING DUPLICATES:")
    print(df.drop_duplicates().shape)

    print("\nUNIQUE VALUES:")
    print(df.nunique())

    print("\nDATA TYPES:")
    print(df.dtypes)

    print("\nINFO:")
    df.info()

    print("\nSTATISTICS:")
    print(df.describe())

    # Add summary to report
    report_data.append({
        "file_name": file.name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "total_missing_values": df.isna().sum().sum(),
        "duplicate_rows": df.duplicated().sum()
    })

# Create report DataFrame
report_df = pd.DataFrame(report_data)

# Save profiling report
report_file = reports_path / "profiling_report.csv"
report_df.to_csv(report_file, index=False)

print("\n" + "=" * 60)
print("PROFILING REPORT SAVED:")
print(report_file)