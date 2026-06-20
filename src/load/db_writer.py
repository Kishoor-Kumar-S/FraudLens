import pandas as pd
from sqlalchemy import create_engine
import os
import logging

logger = logging.getLogger(__name__)

def get_engine():
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://fraud_user:fraud_pass@localhost:5432/fraudlens"
    )
    return create_engine(db_url)

def write_fraud_flags(fraud_df: pd.DataFrame):
    if fraud_df.empty:
        logger.info("No fraud flags to write.")
        return

    engine = get_engine()
    fraud_df.to_sql(
        "fraud_flags",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
    )
    logger.info(f"Written {len(fraud_df)} fraud flags to PostgreSQL.")
