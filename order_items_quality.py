import pandas as pd

df = pd.read_csv("data/raw/olist_order_items_dataset.csv")

print("\nMISSING VALUES:")
print(df.isna().sum())

print("\nDUPLICATES:")
print(df.duplicated().sum())

print("\nDATA TYPES:")
print(df.dtypes)

print("\nINVALID PRICE:")
print(df[df["price"] <= 0][["order_id", "product_id", "price"]])

print("\nINVALID FREIGHT VALUE:")
print(df[df["freight_value"] < 0][["order_id", "product_id", "freight_value"]])

print("\nDUPLICATE ITEM NUMBERS WITHIN SAME ORDER:")

duplicate_items = df.duplicated(
    subset=["order_id", "order_item_id"]
).sum()

print(duplicate_items)

print("\nINVALID SHIPPING DATES:")

dates = pd.to_datetime(
    df["shipping_limit_date"],
    errors="coerce"
)

print("Invalid dates:", dates.isna().sum())