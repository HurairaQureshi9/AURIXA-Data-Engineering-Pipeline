
from pathlib import Path
import logging
import os

import pandas as pd
from sqlalchemy import URL, create_engine, text


# ============================================================
# AURIXA - E-Commerce ETL Loading Pipeline
# ============================================================

# 1. Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
REPORTS_DIR = PROJECT_ROOT / "Reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = REPORTS_DIR / "etl_load.log"


# 2. Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True,
)

logger = logging.getLogger("AURIXA")


# 3. Source CSV files and destination MySQL tables
table_files = [
    ("customers", "olist_customers_cleaned.csv"),
    ("sellers", "olist_sellers_cleaned.csv"),
    ("products", "olist_products_cleaned.csv"),
    (
        "product_category_name_translation",
        "product_category_name_translation_cleaned.csv",
    ),
    ("geolocation", "olist_geolocation_cleaned.csv"),
    ("orders", "olist_orders_cleaned.csv"),
    ("order_items", "olist_order_items_cleaned.csv"),
    ("order_payments", "olist_order_payments_cleaned.csv"),
    ("order_reviews", "olist_order_reviews_cleaned.csv"),
]


# 4. Expected CSV schemas
expected_columns = {
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


# 5. Date columns requiring conversion
date_columns = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "shipping_limit_date",
    ],
    "order_reviews": [
        "review_creation_date",
        "review_answer_timestamp",
    ],
}


# 6. Primary-key definitions
# Geolocation intentionally has no primary key.
primary_keys = {
    "customers": ["customer_id"],
    "sellers": ["seller_id"],
    "products": ["product_id"],
    "product_category_name_translation": [
        "product_category_name"
    ],
    "orders": ["order_id"],
    "order_items": ["order_id", "order_item_id"],
    "order_payments": ["order_id", "payment_sequential"],
    "order_reviews": ["review_id", "order_id"],
}


# 7. Foreign-key relationships to validate before loading
foreign_keys = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
    ("order_items", "seller_id", "sellers", "seller_id"),
    ("order_payments", "order_id", "orders", "order_id"),
    ("order_reviews", "order_id", "orders", "order_id"),
]


def create_db_engine():
    """Create a MySQL connection without hardcoding credentials."""

    db_user = os.getenv("AURIXA_DB_USER", "root")
    db_password = os.getenv("AURIXA_DB_PASSWORD")

    if not db_password:
        raise RuntimeError(
            "AURIXA_DB_PASSWORD is not set. "
            "Set the database password in your terminal first."
        )

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host="localhost",
        port=3306,
        database="aurixa_db",
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True,
    )


def prepare_datasets():
    """Extract cleaned CSVs and validate their schemas and keys."""

    datasets = {}

    for table, filename in table_files:
        file_path = CLEANED_DIR / filename

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Cleaned CSV file not found: {file_path}"
            )

        df = pd.read_csv(file_path)

        # Validate column names and their order.
        expected = expected_columns[table]

        if list(df.columns) != expected:
            raise ValueError(
                f"Schema mismatch in {filename}. "
                f"Expected columns: {expected}. "
                f"Found columns: {list(df.columns)}"
            )

        # Convert date columns and reject invalid date strings.
        for column in date_columns.get(table, []):
            original = df[column]
            converted = pd.to_datetime(
                original,
                errors="coerce",
            )

            invalid_dates = original.notna() & converted.isna()

            if invalid_dates.any():
                raise ValueError(
                    f"Invalid dates found in {table}.{column}: "
                    f"{int(invalid_dates.sum())} row(s)"
                )

            df[column] = converted

        # Validate primary-key columns and uniqueness.
        keys = primary_keys.get(table, [])

        if keys:
            if df[keys].isna().any().any():
                raise ValueError(
                    f"NULL primary-key values found in {table}"
                )

            if df.duplicated(subset=keys).any():
                raise ValueError(
                    f"Duplicate primary-key values found in {table}"
                )

        datasets[table] = df

        logger.info(
            "Prepared %s | rows=%s | columns=%s",
            table,
            len(df),
            len(df.columns),
        )

    return datasets


def validate_relationships(datasets):
    """Check that child-table keys have matching parent records."""

    for child_table, child_column, parent_table, parent_column in foreign_keys:
        child_df = datasets[child_table]
        parent_df = datasets[parent_table]

        if child_df[child_column].isna().any():
            raise ValueError(
                f"NULL foreign-key values found in "
                f"{child_table}.{child_column}"
            )

        parent_values = parent_df[parent_column]

        unmatched = ~child_df[child_column].isin(parent_values)

        if unmatched.any():
            raise ValueError(
                f"Foreign-key validation failed: "
                f"{child_table}.{child_column} has "
                f"{int(unmatched.sum())} unmatched row(s) "
                f"against {parent_table}.{parent_column}"
            )

        logger.info(
            "Relationship validated: %s.%s -> %s.%s",
            child_table,
            child_column,
            parent_table,
            parent_column,
        )


def load_datasets(engine, datasets):
    """Load all tables transactionally and verify their row counts."""

    with engine.begin() as connection:

        # Safety guard: never append to already-populated tables.
        existing_tables = []

        for table, _ in table_files:
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM `{table}`")
            ).scalar_one()

            if count > 0:
                existing_tables.append(f"{table} ({count} rows)")

        if existing_tables:
            raise RuntimeError(
                "Loading cancelled to prevent duplicate records. "
                "These target tables already contain data: "
                + ", ".join(existing_tables)
                + ". Use an empty destination database for a fresh load."
            )

        logger.info("All target tables are empty. Starting ETL load.")

        # Parent tables are listed before dependent tables.
        for table, _ in table_files:
            df = datasets[table]

            df.to_sql(
                name=table,
                con=connection,
                if_exists="append",
                index=False,
                chunksize=5000,
            )

            logger.info(
                "Loaded %s | rows=%s",
                table,
                len(df),
            )

        # Verify loaded row counts before the transaction completes.
        logger.info("Starting row-count validation.")

        for table, _ in table_files:
            actual_count = connection.execute(
                text(f"SELECT COUNT(*) FROM `{table}`")
            ).scalar_one()

            expected_count = len(datasets[table])

            if actual_count != expected_count:
                raise RuntimeError(
                    f"Row-count mismatch in {table}: "
                    f"expected {expected_count}, "
                    f"found {actual_count}"
                )

            logger.info(
                "Validated %s | expected=%s | actual=%s",
                table,
                expected_count,
                actual_count,
            )

    logger.info("ETL loading and row-count validation completed.")


def main():
    """Run the complete AURIXA ETL loading workflow."""

    logger.info("AURIXA ETL pipeline started.")

    engine = None

    try:
        # Extract and validate source data first.
        datasets = prepare_datasets()

        # Validate relationships between source datasets.
        validate_relationships(datasets)

        # Connect only after source validation passes.
        engine = create_db_engine()

        with engine.connect() as connection:
            database_name = connection.execute(
                text("SELECT DATABASE()")
            ).scalar_one()

            if database_name != "aurixa_db":
                raise RuntimeError(
                    f"Unexpected database selected: {database_name}"
                )

        logger.info("Connected to database: %s", database_name)

        # Load and validate target tables.
        load_datasets(engine, datasets)

        print("\nETL pipeline completed successfully.")
        print(f"Log file: {LOG_FILE}")

    except Exception:
        logger.exception("AURIXA ETL pipeline failed.")
        raise

    finally:
        if engine is not None:
            engine.dispose()


if __name__ == "__main__":
    main()
