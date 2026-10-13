import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - SELLERS CLEANING
# ==============================

INPUT_FILE = Path("data/raw/olist_sellers_dataset.csv")
OUTPUT_FILE = Path("data/cleaned/olist_sellers_cleaned.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - SELLERS DATA CLEANING")
print("=" * 40)

print("\nOriginal dataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types BEFORE cleaning:")
print(df.dtypes)

print("\nMissing values BEFORE cleaning:")
print(df.isnull().sum())

print("\nDuplicate seller IDs:")
print(df["seller_id"].duplicated().sum())

print("\nDuplicate complete rows:")
print(df.duplicated().sum())

# ==============================
# CLEANING
# ==============================

# Clean city and state text
df["seller_city"] = df["seller_city"].str.strip()
df["seller_state"] = df["seller_state"].str.strip()

# ==============================
# AFTER CLEANING
# ==============================

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nDuplicate seller IDs AFTER cleaning:")
print(df["seller_id"].duplicated().sum())

print("\nDuplicate complete rows AFTER cleaning:")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nSellers cleaning completed successfully!")