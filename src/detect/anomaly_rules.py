import pandas as pd
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

RULES = {
    "AMOUNT_SPIKE":       lambda df: df["spike_ratio"] > 3,
    "HIGH_FREQUENCY":     lambda df: df["txn_count_per_hour"] > 10,
    "FAILED_LOGIN_SPIKE": lambda df: df["failed_logins"] > 3,
    "LOCATION_MISMATCH":  lambda df: df["location_mismatch"] == 1,
    "ODD_HOURS":          lambda df: df["is_odd_hour"] == 1,
}

RISK_WEIGHTS = {
    "AMOUNT_SPIKE":       40,
    "HIGH_FREQUENCY":     30,
    "FAILED_LOGIN_SPIKE": 35,
    "LOCATION_MISMATCH":  25,
    "ODD_HOURS":          15,
}

def apply_rules(df: pd.DataFrame) -> pd.DataFrame:
    flags: List[Dict] = []

    for rule_name, rule_fn in RULES.items():
        triggered = df[rule_fn(df)].copy()
        triggered["rule_triggered"] = rule_name
        triggered["risk_score"]     = RISK_WEIGHTS[rule_name]
        flags.append(triggered[["transaction_id", "customer_id", "rule_triggered", "risk_score"]])
        logger.info(f"Rule [{rule_name}] flagged {len(triggered)} transactions.")

    if not flags:
        return pd.DataFrame()

    fraud_df = pd.concat(flags, ignore_index=True)

    # Aggregate risk score per transaction
    risk_summary = (
        fraud_df.groupby("transaction_id")
                .agg(
                    customer_id=("customer_id", "first"),
                    rules_triggered=("rule_triggered", lambda x: ", ".join(x)),
                    total_risk_score=("risk_score", "sum"),
                )
                .reset_index()
    )

    logger.info(f"Total flagged transactions: {len(risk_summary)}")
    return risk_summary
