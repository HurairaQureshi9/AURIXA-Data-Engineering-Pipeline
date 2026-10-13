
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DIR = PROJECT_ROOT / "DATA" / "cleaned"

EXPECTED_COLUMNS = {
    "customers": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "sellers": [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
    ],
    "products": [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "product_category_name_translation": [
        "product_category_name",
        "product_category_name_english",
    ],
    "geolocation": [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "order_payments": [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    ],
    "order_reviews": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ],
}

PRIMARY_KEYS = {
    "customers": ["customer_id"],
    "sellers": ["seller_id"],
    "products": ["product_id"],
    "product_category_name_translation": ["product_category_name"],
    "orders": ["order_id"],
    "order_items": ["order_id", "order_item_id"],
    "order_payments": ["order_id", "payment_sequential"],
    "order_reviews": ["review_id", "order_id"],
}

DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": ["shipping_limit_date"],
    "order_reviews": [
        "review_creation_date",
        "review_answer_timestamp",
    ],
}

FAILED_CHECKS = 0

print("=" * 60)
print("AURIXA - ETL PIPELINE VALIDATION")
print("=" * 60)

for table, expected_columns in EXPECTED_COLUMNS.items():
    filename = f"olist_{table}_cleaned.csv"
    if table == "product_category_name_translation":
        filename = "product_category_name_translation_cleaned.csv"

    file_path = CLEANED_DIR / filename

    print(f"\nChecking: {filename}")

    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path)

        missing_columns = [
            col for col in expected_columns if col not in df.columns
        ]
        unexpected_columns = [
            col for col in df.columns if col not in expected_columns
        ]

        if missing_columns or unexpected_columns:
            FAILED_CHECKS += 1
            print("FAIL: Column schema mismatch")
            if missing_columns:
                print(f"Missing columns: {missing_columns}")
            if unexpected_columns:
                print(f"Unexpected columns: {unexpected_columns}")
            continue

        if df.empty:
            FAILED_CHECKS += 1
            print("FAIL: CSV contains no rows")
            continue

        key_columns = PRIMARY_KEYS.get(table, [])
        if key_columns:
            if df[key_columns].isna().any().any():
                FAILED_CHECKS += 1
                print(f"FAIL: NULL values in key columns: {key_columns}")
                continue

            if df.duplicated(subset=key_columns).any():
                FAILED_CHECKS += 1
                print(f"FAIL: Duplicate key values: {key_columns}")
                continue

        for column in DATE_COLUMNS.get(table, []):
            original = df[column]
            parsed = pd.to_datetime(original, errors="coerce")
            invalid = original.notna() & parsed.isna()

            if invalid.any():
                FAILED_CHECKS += 1
                print(
                    f"FAIL: {invalid.sum()} invalid date values "
                    f"in {column}"
                )
                break
        else:
            print(f"PASS: {len(df):,} rows | {len(df.columns)} columns")
            continue

    except Exception as error:
        FAILED_CHECKS += 1
        print(f"FAIL: {error}")

print("\n" + "=" * 60)
if FAILED_CHECKS == 0:
    print("RESULT: ALL VALIDATION CHECKS PASSED")
else:
    print(f"RESULT: {FAILED_CHECKS} CHECK(S) FAILED")
print("=" * 60)
print("No MySQL data was modified.")

