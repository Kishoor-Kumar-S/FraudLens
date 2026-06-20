-- ─────────────────────────────────────────────────────────────
-- FraudLens: Window Function Analytics
-- ─────────────────────────────────────────────────────────────

-- 1. Running total per customer
SELECT
    transaction_id,
    customer_id,
    amount,
    transaction_time,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY transaction_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM transactions;

-- 2. Transaction rank by amount per customer
SELECT
    transaction_id,
    customer_id,
    amount,
    RANK() OVER (
        PARTITION BY customer_id
        ORDER BY amount DESC
    ) AS amount_rank
FROM transactions;

-- 3. Rolling 7-day fraud flag count per customer
SELECT
    customer_id,
    flagged_at::DATE AS flag_date,
    COUNT(*) OVER (
        PARTITION BY customer_id
        ORDER BY flagged_at::DATE
        RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW
    ) AS rolling_7day_flags
FROM fraud_flags;

-- 4. Lag/Lead: Time between consecutive transactions
SELECT
    transaction_id,
    customer_id,
    transaction_time,
    LAG(transaction_time) OVER (
        PARTITION BY customer_id
        ORDER BY transaction_time
    ) AS prev_txn_time,
    EXTRACT(EPOCH FROM (
        transaction_time - LAG(transaction_time) OVER (
            PARTITION BY customer_id ORDER BY transaction_time
        )
    )) / 60 AS minutes_since_last_txn
FROM transactions;

-- 5. Percentile-based anomaly scoring
SELECT
    transaction_id,
    customer_id,
    amount,
    PERCENT_RANK() OVER (
        PARTITION BY customer_id
        ORDER BY amount
    ) AS amount_percentile
FROM transactions;
