import pandas as pd

df = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

print("\nMISSING VALUES:")
print(df.isna().sum())

print("\nDUPLICATES:")
print(df.duplicated().sum())

print("\nDATA TYPES:")
print(df.dtypes)

print("\nINVALID PAYMENT VALUE:")
print(df[df["payment_value"] < 0][
    ["order_id", "payment_type", "payment_value"]
])

print("\nINVALID INSTALLMENTS:")
print(df[df["payment_installments"] < 0][
    ["order_id", "payment_type", "payment_installments"]
])

print("\nPAYMENT TYPES:")
print(df["payment_type"].value_counts())

print("\nINSTALLMENTS:")
print(df["payment_installments"].value_counts().sort_index())

print("\nNOT DEFINED PAYMENT TYPE:")
print(
    df[df["payment_type"] == "not_defined"]
)

print("\nZERO INSTALLMENTS:")
print(
    df[df["payment_installments"] == 0]
)