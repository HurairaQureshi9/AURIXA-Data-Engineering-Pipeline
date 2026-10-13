import pandas as pd

df = pd.read_csv("data/raw/olist_products_dataset.csv")

print("\nMISSING VALUES:")
print(df.isna().sum())

print("\nROWS WITH MISSING VALUES:")
print(df[df.isna().any(axis=1)].head(10))

print("\nMISSING VALUES BY COLUMN TOGETHER:")
print(
    df[
        [
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ].isna().sum(axis=1).value_counts().sort_index()
)

print("\nMISSING 4 PRODUCT FIELDS TOGETHER:")

print(
    df[
        [
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty"
        ]
    ].isna().all(axis=1).sum()
)

print("\nMISSING DIMENSION/WEIGHT FIELDS:")
print(
    df[
        [
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ].isna().sum()
)

print("\nDATA TYPES:")
print(df.dtypes)

print("\nINVALID NUMERIC VALUES:")

print("\nWeight <= 0:")
print(df[df["product_weight_g"] <= 0][["product_id", "product_weight_g"]])

print("\nLength <= 0:")
print(df[df["product_length_cm"] <= 0][["product_id", "product_length_cm"]])

print("\nHeight <= 0:")
print(df[df["product_height_cm"] <= 0][["product_id", "product_height_cm"]])

print("\nWidth <= 0:")
print(df[df["product_width_cm"] <= 0][["product_id", "product_width_cm"]])

print("\nINVALID PRODUCT INFORMATION VALUES:")

print("\nName length <= 0:")
print(df[df["product_name_lenght"] <= 0][
    ["product_id", "product_name_lenght"]
])

print("\nDescription length <= 0:")
print(df[df["product_description_lenght"] <= 0][
    ["product_id", "product_description_lenght"]
])

print("\nPhotos quantity <= 0:")
print(df[df["product_photos_qty"] <= 0][
    ["product_id", "product_photos_qty"]
])

print("\nDUPLICATE PRODUCT IDs:")
print(df["product_id"].duplicated().sum())

print("\nUNIQUE PRODUCT IDs:")
print(df["product_id"].nunique())

print("\nTOTAL ROWS:")
print(len(df))