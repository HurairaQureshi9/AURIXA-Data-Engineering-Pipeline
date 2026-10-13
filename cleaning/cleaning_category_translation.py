import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - CATEGORY TRANSLATION CLEANING
# ==============================

INPUT_FILE = Path("data/raw/product_category_name_translation.csv")
OUTPUT_FILE = Path("data/cleaned/product_category_name_translation_cleaned.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - CATEGORY TRANSLATION DATA CLEANING")
print("=" * 45)

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

# Remove extra spaces from text columns
for column in df.columns:
    df[column] = df[column].str.strip()

# Remove duplicate rows
df = df.drop_duplicates()

# ==============================
# AFTER CLEANING
# ==============================

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nDuplicate complete rows AFTER cleaning:")
print(df.duplicated().sum())

print("\nFinal dataset shape:")
print(df.shape)

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nCategory translation cleaning completed successfully!")