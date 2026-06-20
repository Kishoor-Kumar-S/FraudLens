# 🔍 FraudLens — Fraud Analytics & Detection System

> A rule-based fraud analytics system built with Python, SQL, PostgreSQL, Pandas, Streamlit, and Power BI to detect suspicious transaction patterns across high-volume financial datasets.

---

## 📌 Project Overview

FraudLens is a **fraud detection and analytics platform** that ingests raw financial transaction data, applies rule-based anomaly detection logic, stores flagged results in PostgreSQL, and surfaces insights through interactive Streamlit and Power BI dashboards.

---

## 🏗️ Architecture

```
Raw Transactions (CSV/DB)
        │
        ▼
  Python + Pandas (Data Processing)
        │
        ▼
  Rule-Based Anomaly Detection Engine
        │
        ▼
  SQL + PostgreSQL (Fraud Monitoring & Window Functions)
        │
        ├──► Streamlit Dashboard (Real-time Alerts)
        └──► Power BI Dashboard (Executive Reporting)
```

---

## 🗂️ Project Structure

```
FraudLens/
├── src/
│   ├── extract/
│   │   └── data_loader.py          # Raw transaction ingestion
│   ├── transform/
│   │   └── preprocess.py           # Data cleaning & feature engineering
│   ├── detect/
│   │   └── anomaly_rules.py        # Rule-based fraud detection engine
│   └── load/
│       └── db_writer.py            # PostgreSQL writer
├── sql/
│   ├── schema.sql                  # Table definitions
│   ├── fraud_detection_queries.sql # Core fraud SQL queries
│   └── window_functions.sql        # Window function analytics
├── dashboard/
│   └── app.py                      # Streamlit dashboard
├── data/
│   ├── raw/                        # Raw transaction datasets
│   └── processed/                  # Flagged & cleaned data
├── config/
│   └── config.yaml                 # Project configuration
├── tests/
│   └── test_detection.py           # Unit tests
├── requirements.txt
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Data Processing | Python, Pandas |
| Detection Engine | Rule-Based Anomaly Detection |
| Database | PostgreSQL |
| Analytics | SQL, Window Functions |
| Visualization | Streamlit, Power BI |
| Storage | PostgreSQL, CSV |

---

## 🚨 Fraud Detection Rules

| Rule | Description |
|---|---|
| **Amount Spike** | Transaction amount > 3× customer average |
| **High Frequency** | >10 transactions within 1 hour |
| **Failed Logins** | >3 failed login attempts before transaction |
| **Location Mismatch** | Transaction country ≠ registered country |
| **Odd Hours** | Transactions between 12AM–4AM |
| **New Device** | First-time device fingerprint |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 14+
- Docker & Docker Compose (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/Kishoor-Kumar-S/FraudLens.git
cd FraudLens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running with Docker

```bash
docker-compose up -d
```

### Setup Database

```bash
psql -U postgres -d fraudlens -f sql/schema.sql
```

### Run Detection Pipeline

```bash
python src/extract/data_loader.py
python src/transform/preprocess.py
python src/detect/anomaly_rules.py
python src/load/db_writer.py
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 📊 Dashboard Features

- **Fraud Trend Analysis** — Daily/weekly flagged transaction counts
- **Suspicious Accounts** — High-risk customer leaderboard
- **Transaction Heatmap** — Time-of-day fraud concentration
- **Rule Breakdown** — Which rules triggered most flags
- **Alert Summary** — Real-time investigative queue for analysts

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🔑 Key Highlights

- ✅ **Rule-based anomaly detection** across 6 fraud signal types
- ✅ **Optimized SQL window functions** for customer-level trend monitoring
- ✅ **Pandas pipelines** for transaction frequency and spike analysis
- ✅ **Streamlit** real-time alert dashboard for fraud analysts
- ✅ **Power BI** executive reporting dashboard

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Kishoor** — B.Tech AI & Data Science, Chennai Institute of Technology  
[LinkedIn](https://linkedin.com/in/your-profile) • [GitHub](https://github.com/Kishoor-Kumar-S)
