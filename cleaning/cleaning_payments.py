import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - PAYMENTS CLEANING
# ==============================

INPUT_FILE = Path("data/raw/olist_order_payments_dataset.csv")
OUTPUT_FILE = Path("data/cleaned/olist_order_payments_cleaned.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - PAYMENTS DATA CLEANING")
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

# Clean payment type text
df["payment_type"] = df["payment_type"].str.strip().str.lower()

# Check numeric columns
df["payment_installments"] = pd.to_numeric(
    df["payment_installments"],
    errors="coerce"
)

df["payment_value"] = pd.to_numeric(
    df["payment_value"],
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

print("\nPayment types:")
print(df["payment_type"].value_counts())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nPayments cleaning completed successfully!")