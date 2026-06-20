-- ─────────────────────────────────────────────────────────────
-- FraudLens: Core Fraud Detection SQL Queries
-- ─────────────────────────────────────────────────────────────

-- 1. Amount Spike Detection (> 3x customer average)
SELECT
    t.transaction_id,
    t.customer_id,
    t.amount,
    c.avg_transaction_amt,
    ROUND(t.amount / NULLIF(c.avg_transaction_amt, 0), 2) AS spike_ratio,
    'AMOUNT_SPIKE' AS rule_triggered
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.amount > 3 * c.avg_transaction_amt;

-- 2. High Frequency Transactions (> 10 within 1 hour)
SELECT
    customer_id,
    DATE_TRUNC('hour', transaction_time) AS hour_window,
    COUNT(*) AS txn_count,
    'HIGH_FREQUENCY' AS rule_triggered
FROM transactions
GROUP BY customer_id, DATE_TRUNC('hour', transaction_time)
HAVING COUNT(*) > 10;

-- 3. Failed Login Anomaly (> 3 failed logins before transaction)
SELECT
    transaction_id,
    customer_id,
    failed_logins,
    amount,
    'FAILED_LOGIN_SPIKE' AS rule_triggered
FROM transactions
WHERE failed_logins > 3;

-- 4. Location Mismatch
SELECT
    t.transaction_id,
    t.customer_id,
    t.country AS txn_country,
    c.registered_country,
    'LOCATION_MISMATCH' AS rule_triggered
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
WHERE t.country <> c.registered_country;

-- 5. Odd Hours Transactions (12AM - 4AM)
SELECT
    transaction_id,
    customer_id,
    transaction_time,
    amount,
    'ODD_HOURS' AS rule_triggered
FROM transactions
WHERE EXTRACT(HOUR FROM transaction_time) BETWEEN 0 AND 4;

-- 6. High-Risk Account Summary
SELECT
    customer_id,
    COUNT(*)          AS total_flags,
    MAX(risk_score)   AS max_risk_score,
    MIN(flagged_at)   AS first_flag,
    MAX(flagged_at)   AS latest_flag
FROM fraud_flags
WHERE reviewed = FALSE
GROUP BY customer_id
ORDER BY total_flags DESC;
