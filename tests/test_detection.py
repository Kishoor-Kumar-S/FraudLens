import pytest
import pandas as pd
from src.detect.anomaly_rules import apply_rules

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "transaction_id":     ["T001", "T002", "T003", "T004", "T005"],
        "customer_id":        ["C001", "C002", "C003", "C004", "C005"],
        "amount":             [5000, 200, 300, 150, 800],
        "avg_transaction_amt":[100,  200, 300, 150, 100],
        "spike_ratio":        [50.0, 1.0, 1.0, 1.0, 8.0],
        "txn_count_per_hour": [2,    15,  3,   2,   2],
        "failed_logins":      [0,    0,   5,   0,   0],
        "location_mismatch":  [0,    0,   0,   1,   0],
        "is_odd_hour":        [0,    0,   0,   0,   1],
        "country":            ["IN", "IN", "US", "UK", "IN"],
        "registered_country": ["IN", "IN", "IN", "IN", "IN"],
    })

def test_amount_spike_detected(sample_df):
    result = apply_rules(sample_df)
    assert "T001" in result["transaction_id"].values

def test_high_frequency_detected(sample_df):
    result = apply_rules(sample_df)
    assert "T002" in result["transaction_id"].values

def test_failed_login_detected(sample_df):
    result = apply_rules(sample_df)
    assert "T003" in result["transaction_id"].values

def test_location_mismatch_detected(sample_df):
    result = apply_rules(sample_df)
    assert "T004" in result["transaction_id"].values

def test_odd_hours_detected(sample_df):
    result = apply_rules(sample_df)
    assert "T005" in result["transaction_id"].values

def test_risk_score_positive(sample_df):
    result = apply_rules(sample_df)
    assert (result["total_risk_score"] > 0).all()
