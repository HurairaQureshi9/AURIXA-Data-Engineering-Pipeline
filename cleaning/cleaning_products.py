import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - PRODUCTS CLEANING
# ==============================

# Input file
INPUT_FILE = Path("data/raw/olist_products_dataset.csv")

# Output file
OUTPUT_FILE = Path("data/cleaned/olist_products_cleaned.csv")

# Create cleaned folder if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Read raw data
df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - PRODUCTS DATA CLEANING")
print("=" * 40)

# Basic information
print("\nOriginal dataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

# Missing values before cleaning
print("\nMissing values BEFORE cleaning:")
print(df.isnull().sum())

# Duplicate checks
print("\nDuplicate product IDs:")
print(df["product_id"].duplicated().sum())

print("\nDuplicate complete rows:")
print(df.duplicated().sum())

# ==============================
# CLEANING
# ==============================

# Category missing values
df["product_category_name"] = df["product_category_name"].fillna("Unknown")

# Product information missing values
df["product_name_lenght"] = df["product_name_lenght"].fillna(0)
df["product_description_lenght"] = df["product_description_lenght"].fillna(0)
df["product_photos_qty"] = df["product_photos_qty"].fillna(0)

# Physical measurements are left missing
# because we should not invent unknown measurements.

# ==============================
# AFTER CLEANING
# ==============================

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nDuplicate product IDs AFTER cleaning:")
print(df["product_id"].duplicated().sum())

print("\nDuplicate complete rows AFTER cleaning:")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nProducts cleaning completed successfully!")