import pandas as pd
from pathlib import Path

# ==============================
# AURIXA - REVIEWS CLEANING
# ==============================

INPUT_FILE = Path("data/raw/olist_order_reviews_dataset.csv")
OUTPUT_FILE = Path("data/cleaned/olist_order_reviews_cleaned.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("\nAURIXA - REVIEWS DATA CLEANING")
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

# Convert review creation and answer dates
df["review_creation_date"] = pd.to_datetime(
    df["review_creation_date"],
    errors="coerce"
)

df["review_answer_timestamp"] = pd.to_datetime(
    df["review_answer_timestamp"],
    errors="coerce"
)

# Clean review comment text
df["review_comment_title"] = df["review_comment_title"].fillna("")
df["review_comment_message"] = df["review_comment_message"].fillna("")

df["review_comment_title"] = df["review_comment_title"].str.strip()
df["review_comment_message"] = df["review_comment_message"].str.strip()

# ==============================
# AFTER CLEANING
# ==============================

print("\nData types AFTER cleaning:")
print(df.dtypes)

print("\nMissing values AFTER cleaning:")
print(df.isnull().sum())

print("\nDuplicate complete rows AFTER cleaning:")
print(df.duplicated().sum())

print("\nReview score distribution:")
print(df["review_score"].value_counts().sort_index())

# Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned file saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:")
print(df.shape)

print("\nReviews cleaning completed successfully!")