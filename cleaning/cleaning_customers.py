import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - CUSTOMERS CLEANING
# ==============================

# Input file
INPUT_FILE = Path("data/raw/olist_customers_dataset.csv")

# Output file
OUTPUT_FILE = Path("data/cleaned/olist_customers_cleaned.csv")

# Create cleaned folder if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Read raw data
df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - CUSTOMERS DATA CLEANING")
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
print("\nDuplicate customer IDs:")
print(df["customer_id"].duplicated().sum())

print("\nDuplicate customer unique IDs:")
print(df["customer_unique_id"].duplicated().sum())

print("\nDuplicate complete rows:")
print(df.duplicated().sum())

# ==============================
# CLEANING
# ==============================

# Remove extra spaces from text columns
df["customer_city"] = df["customer_city"].str.strip()
df["customer_state"] = df["customer_state"].str.strip()

# ==============================
# AFTER CLEANING
# ==============================

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nDuplicate customer IDs AFTER cleaning:")
print(df["customer_id"].duplicated().sum())

print("\nDuplicate customer unique IDs AFTER cleaning:")
print(df["customer_unique_id"].duplicated().sum())

print("\nDuplicate complete rows AFTER cleaning:")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nCustomers cleaning completed successfully!")