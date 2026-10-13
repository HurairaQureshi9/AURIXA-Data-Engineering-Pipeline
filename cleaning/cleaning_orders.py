import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - ORDERS CLEANING
# ==============================

# Input file
INPUT_FILE = Path("data/raw/olist_orders_dataset.csv")

# Output file
OUTPUT_FILE = Path("data/cleaned/olist_orders_cleaned.csv")

# Create cleaned folder if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Read raw data
df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - ORDERS DATA CLEANING")
print("=" * 40)

# Basic information
print("\nOriginal dataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types BEFORE cleaning:")
print(df.dtypes)

# Missing values before cleaning
print("\nMissing values BEFORE cleaning:")
print(df.isnull().sum())

# Duplicate checks
print("\nDuplicate order IDs:")
print(df["order_id"].duplicated().sum())

print("\nDuplicate complete rows:")
print(df.duplicated().sum())

# Order status check
print("\nOrder status counts:")
print(df["order_status"].value_counts())

# ==============================
# CLEANING
# ==============================

# Convert date columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")

# ==============================
# AFTER CLEANING
# ==============================

print("\nData types AFTER cleaning:")
print(df.dtypes)

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nDuplicate order IDs AFTER cleaning:")
print(df["order_id"].duplicated().sum())

print("\nDuplicate complete rows AFTER cleaning:")
print(df.duplicated().sum())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nOrders cleaning completed successfully!")