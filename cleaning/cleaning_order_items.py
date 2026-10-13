import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - ORDER ITEMS CLEANING
# ==============================

INPUT_FILE = Path("data/raw/olist_order_items_dataset.csv")
OUTPUT_FILE = Path("data/cleaned/olist_order_items_cleaned.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - ORDER ITEMS DATA CLEANING")
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

print("\nDuplicate order_id + order_item_id:")
print(df.duplicated(subset=["order_id", "order_item_id"]).sum())

# ==============================
# CLEANING
# ==============================

# Convert shipping_limit_date to datetime
df["shipping_limit_date"] = pd.to_datetime(
    df["shipping_limit_date"],
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

print("\nDuplicate order_id + order_item_id AFTER cleaning:")
print(df.duplicated(
    subset=["order_id", "order_item_id"]
).sum())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nOrder items cleaning completed successfully!")