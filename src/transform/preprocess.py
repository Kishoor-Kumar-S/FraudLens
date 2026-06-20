import pandas as pd
import logging

logger = logging.getLogger(__name__)

def preprocess(transactions: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    # Merge customer profile
    df = transactions.merge(customers, on="customer_id", how="left")

    # Feature engineering
    df["hour"]          = df["transaction_time"].dt.hour
    df["day_of_week"]   = df["transaction_time"].dt.dayofweek
    df["spike_ratio"]   = df["amount"] / df["avg_transaction_amt"].replace(0, 1)
    df["is_odd_hour"]   = df["hour"].between(0, 4).astype(int)
    df["location_mismatch"] = (df["country"] != df["registered_country"]).astype(int)

    # Transaction frequency per customer per hour
    df["hour_window"] = df["transaction_time"].dt.floor("H")
    freq = (
        df.groupby(["customer_id", "hour_window"])
          .size()
          .reset_index(name="txn_count_per_hour")
    )
    df = df.merge(freq, on=["customer_id", "hour_window"], how="left")

    logger.info(f"Preprocessed {len(df)} records with {df.shape[1]} features.")
    return df
