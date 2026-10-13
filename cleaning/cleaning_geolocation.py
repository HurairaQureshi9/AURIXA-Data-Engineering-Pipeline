import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - GEOLOCATION CLEANING
# ==============================

INPUT_FILE = Path("data/raw/olist_geolocation_dataset.csv")
OUTPUT_FILE = Path("data/cleaned/olist_geolocation_cleaned.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - GEOLOCATION DATA CLEANING")
print("=" * 40)

print("\nOriginal dataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types BEFORE cleaning:")
print(df.dtypes)

print("\nMissing values BEFORE cleaning:")
print(df.isnull().sum())

print("\nDuplicate complete rows:")
print(df.duplicated().sum())

# ==============================
# CLEANING
# ==============================

# Clean text columns
df["geolocation_city"] = df["geolocation_city"].str.strip()
df["geolocation_state"] = df["geolocation_state"].str.strip()

# Convert latitude and longitude to numeric
df["geolocation_lat"] = pd.to_numeric(
    df["geolocation_lat"],
    errors="coerce"
)

df["geolocation_lng"] = pd.to_numeric(
    df["geolocation_lng"],
    errors="coerce"
)

# ==============================
# AFTER CLEANING
# ==============================

print("\nData types AFTER cleaning:")
print(df.dtypes)

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nDuplicate complete rows AFTER cleaning:")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nGeolocation cleaning completed successfully!")