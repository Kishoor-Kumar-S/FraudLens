import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_transactions(path: str = "data/raw/transactions.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["transaction_time"])
    logger.info(f"Loaded {len(df)} transactions from {path}")
    return df

def load_customers(path: str = "data/raw/customers.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} customer records from {path}")
    return df
