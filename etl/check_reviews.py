from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
file_path = PROJECT_ROOT / "DATA" / "cleaned" / "olist_order_reviews_cleaned.csv"

df = pd.read_csv(file_path)

print("Total rows:", len(df))
print("Unique review IDs:", df["review_id"].nunique())
print("Duplicate review IDs:", df["review_id"].duplicated().sum())

duplicates = df[df["review_id"].duplicated(keep=False)]
print("\nSample duplicate records:")
print(duplicates.sort_values("review_id").head(10).to_string(index=False))