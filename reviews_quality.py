import pandas as pd

df = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")

print("\nREVIEW SCORE DISTRIBUTION:")
print(df["review_score"].value_counts().sort_index())

print("\nMISSING COMMENTS BY REVIEW SCORE:")
print(
    df.groupby("review_score")[
        ["review_comment_title", "review_comment_message"]
    ].apply(lambda x: x.isna().sum())
)

print("\nDATA TYPES:")
print(df.dtypes)

print("\nINVALID REVIEW SCORES:")
print(df[~df["review_score"].between(1, 5)][
    ["review_id", "order_id", "review_score"]
])

print("\nINVALID REVIEW DATES:")

creation_dates = pd.to_datetime(
    df["review_creation_date"],
    errors="coerce"
)

answer_dates = pd.to_datetime(
    df["review_answer_timestamp"],
    errors="coerce"
)

print("Invalid review creation dates:", creation_dates.isna().sum())
print("Invalid review answer dates:", answer_dates.isna().sum())