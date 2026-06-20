-- FraudLens Database Schema

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id      VARCHAR(50) PRIMARY KEY,
    customer_id         VARCHAR(50) NOT NULL,
    amount              DECIMAL(12, 2) NOT NULL,
    transaction_time    TIMESTAMP NOT NULL,
    merchant            VARCHAR(100),
    country             VARCHAR(50),
    device_id           VARCHAR(100),
    failed_logins       INTEGER DEFAULT 0,
    status              VARCHAR(20) DEFAULT 'SUCCESS'
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id         VARCHAR(50) PRIMARY KEY,
    name                VARCHAR(100),
    registered_country  VARCHAR(50),
    account_age_days    INTEGER,
    avg_transaction_amt DECIMAL(12, 2)
);

CREATE TABLE IF NOT EXISTS fraud_flags (
    flag_id             SERIAL PRIMARY KEY,
    transaction_id      VARCHAR(50) REFERENCES transactions(transaction_id),
    customer_id         VARCHAR(50),
    rule_triggered      VARCHAR(100),
    risk_score          INTEGER,
    flagged_at          TIMESTAMP DEFAULT NOW(),
    reviewed            BOOLEAN DEFAULT FALSE
);

-- Indexes for performance
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_time     ON transactions(transaction_time);
CREATE INDEX idx_fraud_flags_customer  ON fraud_flags(customer_id);
CREATE INDEX idx_fraud_flags_reviewed  ON fraud_flags(reviewed);
