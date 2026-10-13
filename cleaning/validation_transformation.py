import pandas as pd
from pathlib import Path

# ==========================================
# AURIXA - VALIDATION & TRANSFORMATION
# ==========================================

CLEANED_FOLDER = Path("data/cleaned")

files = [
    "olist_products_cleaned.csv",
    "olist_customers_cleaned.csv",
    "olist_orders_cleaned.csv",
    "olist_order_items_cleaned.csv",
    "olist_order_payments_cleaned.csv",
    "olist_order_reviews_cleaned.csv",
    "olist_sellers_cleaned.csv",
    "olist_geolocation_cleaned.csv",
    "product_category_name_translation_cleaned.csv"
]

print("\n" + "=" * 60)
print("AURIXA - VALIDATION & TRANSFORMATION")
print("=" * 60)


# ==========================================
# 1. LOAD DATA
# ==========================================

data = {}

for file in files:

    file_path = CLEANED_FOLDER / file

    df = pd.read_csv(file_path)

    data[file] = df

    print(f"\nLoaded: {file}")
    print(f"Shape: {df.shape}")


# ==========================================
# 2. VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("DATA VALIDATION")
print("=" * 60)


for file, df in data.items():

    print("\n" + "-" * 60)
    print(f"FILE: {file}")
    print("-" * 60)

    # Shape
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    # Missing values
    missing = df.isnull().sum()
    total_missing = missing.sum()

    print("Total missing values:", total_missing)

    if total_missing > 0:
        print("\nColumns with missing values:")
        print(missing[missing > 0])

    # Duplicate rows
    duplicate_rows = df.duplicated().sum()

    print("\nDuplicate complete rows:", duplicate_rows)

    # Empty strings
    empty_strings = (df == "").sum().sum()

    print("Empty string values:", empty_strings)


# ==========================================
# 3. PRODUCTS VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("PRODUCTS VALIDATION")
print("=" * 60)

products = data["olist_products_cleaned.csv"]

numeric_product_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

print("\nNegative product values:")

for column in numeric_product_columns:

    negative_count = (products[column] < 0).sum()

    print(f"{column}: {negative_count}")


# ==========================================
# 4. ORDERS VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("ORDERS VALIDATION")
print("=" * 60)

orders = data["olist_orders_cleaned.csv"]

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:

    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

    print(
        f"{column} invalid dates:",
        orders[column].isnull().sum()
    )


# ==========================================
# 5. ORDER ITEMS VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("ORDER ITEMS VALIDATION")
print("=" * 60)

order_items = data["olist_order_items_cleaned.csv"]

print(
    "Negative price values:",
    (order_items["price"] < 0).sum()
)

print(
    "Negative freight values:",
    (order_items["freight_value"] < 0).sum()
)

print(
    "Duplicate order_id + order_item_id:",
    order_items.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)


# ==========================================
# 6. PAYMENTS VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("PAYMENTS VALIDATION")
print("=" * 60)

payments = data["olist_order_payments_cleaned.csv"]

print(
    "Negative payment values:",
    (payments["payment_value"] < 0).sum()
)

print(
    "Invalid installments (less than 1):",
    (payments["payment_installments"] < 1).sum()
)


# ==========================================
# 7. REVIEWS VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("REVIEWS VALIDATION")
print("=" * 60)

reviews = data["olist_order_reviews_cleaned.csv"]

print(
    "Invalid review scores:",
    (
        (reviews["review_score"] < 1) |
        (reviews["review_score"] > 5)
    ).sum()
)


# ==========================================
# 8. GEOLOCATION VALIDATION
# ==========================================

print("\n" + "=" * 60)
print("GEOLOCATION VALIDATION")
print("=" * 60)

geo = data["olist_geolocation_cleaned.csv"]

print("Rows before duplicate removal:", len(geo))

duplicate_geo = geo.duplicated().sum()

print("Exact duplicate rows:", duplicate_geo)

geo = geo.drop_duplicates()

print("Rows after duplicate removal:", len(geo))

print(
    "Invalid latitude:",
    (
        (geo["geolocation_lat"] < -90) |
        (geo["geolocation_lat"] > 90)
    ).sum()
)

print(
    "Invalid longitude:",
    (
        (geo["geolocation_lng"] < -180) |
        (geo["geolocation_lng"] > 180)
    ).sum()
)


# ==========================================
# 9. TRANSFORMATION - TEXT
# ==========================================

print("\n" + "=" * 60)
print("TEXT TRANSFORMATION")
print("=" * 60)


text_files = [
    "olist_products_cleaned.csv",
    "olist_customers_cleaned.csv",
    "olist_order_payments_cleaned.csv",
    "olist_order_reviews_cleaned.csv",
    "olist_sellers_cleaned.csv",
    "olist_geolocation_cleaned.csv",
    "product_category_name_translation_cleaned.csv"
]

for file in text_files:

    df = data[file]

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        df[column] = df[column].astype("string").str.strip()

    data[file] = df


# ==========================================
# 10. TRANSFORMATION - ORDERS DATES
# ==========================================

print("\n" + "=" * 60)
print("DATE TRANSFORMATION")
print("=" * 60)

for column in date_columns:

    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

    # Standard ISO date-time format
    orders[column] = orders[column].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

data["olist_orders_cleaned.csv"] = orders

print("Order date columns standardized.")


# ==========================================
# 11. TRANSFORMATION - SHIPPING DATE
# ==========================================

order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

order_items["shipping_limit_date"] = (
    order_items["shipping_limit_date"]
    .dt.strftime("%Y-%m-%d %H:%M:%S")
)

data["olist_order_items_cleaned.csv"] = order_items

print("Shipping date standardized.")


# ==========================================
# 12. TRANSFORMATION - REVIEW DATES
# ==========================================

for column in [
    "review_creation_date",
    "review_answer_timestamp"
]:

    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )

    reviews[column] = reviews[column].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

data["olist_order_reviews_cleaned.csv"] = reviews

print("Review dates standardized.")


# ==========================================
# 13. SAVE TRANSFORMED DATA
# ==========================================

print("\n" + "=" * 60)
print("SAVING TRANSFORMED DATA")
print("=" * 60)


data["olist_geolocation_cleaned.csv"] = geo


for file, df in data.items():

    output_path = CLEANED_FOLDER / file

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Saved: {file}")


# ==========================================
# 14. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 60)
print("FINAL DATA SUMMARY")
print("=" * 60)

for file, df in data.items():

    print(f"{file}: {df.shape}")


print("\n" + "=" * 60)
print("VALIDATION & TRANSFORMATION COMPLETED!")
print("=" * 60)

# ==========================================
# PAYMENT INSTALLMENT TRANSFORMATION
# ==========================================

print("\n" + "=" * 60)
print("PAYMENT INSTALLMENT TRANSFORMATION")
print("=" * 60)

# Replace invalid 0 installments with 1
invalid_before = (
    payments["payment_installments"] < 1
).sum()

payments.loc[
    payments["payment_installments"] < 1,
    "payment_installments"
] = 1

print("\nInvalid installments before transformation:")
print(invalid_before)

print("\nInvalid installments after transformation:")
print(
    (payments["payment_installments"] < 1).sum()
)

# Save updated payments file
payments.to_csv(
    CLEANED_FOLDER / "olist_order_payments_cleaned.csv",
    index=False
)

print("\nPayment transformation completed!")
print("Payments file saved successfully.")