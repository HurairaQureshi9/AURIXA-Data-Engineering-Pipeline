import pandas as pd

df = pd.read_csv("data/raw/olist_orders_dataset.csv")

print("\nMISSING VALUES BY ORDER STATUS:")

print(
    df.groupby("order_status")[
        [
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ].apply(lambda x: x.isna().sum())
)