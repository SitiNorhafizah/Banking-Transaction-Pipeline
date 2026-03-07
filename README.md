🏦 Banking Transaction ETL & Fraud Analytics Platform

An end-to-end Data Engineering & Analytics project simulating a banking transaction system with:

A PostgreSQL data warehouse (Star Schema)

A production-style ETL pipeline

An interactive Streamlit fraud analytics dashboard

Machine Learning-based fraud scoring

Filtered reporting and downloadable CSV exports

This project demonstrates the complete data lifecycle: ingestion → transformation → storage → analytics → visualization.

🚀 Project Objective

Simulate a real-world banking environment where raw transaction data is:

Extracted from CSV files

Transformed into dimensional models

Loaded into a PostgreSQL data warehouse

Visualized through an interactive Streamlit dashboard

Supports fraud detection, risk scoring, and filtered reporting for stakeholders.

🏗 System Architecture
Raw CSV
   ↓
Python ETL (Pandas + SQLAlchemy)
   ↓
PostgreSQL Data Warehouse (Star Schema)
   ↓
Streamlit Dashboard (Interactive Analytics)
🧱 Data Warehouse Design

Star Schema

Dimension Tables:

dim_customer

dim_account

dim_merchant

dim_location

Fact Table:

fact_transactions

transaction_id

account_id

merchant_id

amount

timestamp

fraud_flag

fraud_score

ETL Guarantees:

✅ Idempotent loads (no duplicate inserts)

✅ Referential integrity

✅ Clean dimensional modeling

✅ Structured transformation logic

📊 Dashboard Features

Built with Streamlit + Plotly

Key Metrics (KPIs)

Total Transactions

Total Transaction Amount

Fraud Cases

Max & Avg Fraud Score

Daily Transaction Volume

Interactive line chart

Hover tooltips

Dynamic filtering

Fraud Alerts

High-risk transactions flagged

ML-based fraud score displayed

Top Risky Accounts & Merchants

Average fraud score by account/merchant

Filters

Account ID

Merchant

Location

Date Range

Downloadable Reports

Export filtered transactions as CSV

🤖 Machine Learning Integration

Fraud prediction model trained on historical transactions

Generates fraud_score for new transactions

Highlights high-risk transactions in the dashboard

🛠 Tech Stack

Backend / ETL: Python, Pandas, SQLAlchemy

Database: PostgreSQL

Visualization: Streamlit, Plotly

Environment: Virtual Environment (venv)

📂 Repository Structure
Banking-Transaction-Pipeline/
│
├── data/                  # Raw transaction CSV files
├── etl/                   # ETL scripts
│   ├── load_from_csv.py
│   ├── etl_phase2.py
│   └── reset.py
├── ml/                    # ML training & scoring
│   ├── train_model.py
│   └── score_model.py
├── dashboard/             # Streamlit dashboard
│   └── app.py
├── requirements.txt
├── .gitignore
└── README.md
⚙ How to Run Locally

1️⃣ Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Setup PostgreSQL Database

CREATE DATABASE banking_dw;

4️⃣ Run ETL Pipeline

python etl/load_from_csv.py

5️⃣ Train ML Model (Optional)

python ml/train_model.py

6️⃣ Launch Dashboard

streamlit run dashboard/app.py
🔐 Environment Variables

Create a .env file in the project root:

DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banking_dw

The .env file is ignored by git for security.

🎯 Skills Demonstrated

Data Warehouse Modeling (Star Schema)

ETL Pipeline Design

Incremental & Idempotent Loading

SQL Joins & Foreign Keys

Data Validation

Fraud Risk Scoring Logic

Interactive Dashboard Development

Production-style Project Structure

🔮 Future Enhancements

🐳 Docker containerization

⏰ Apache Airflow DAG scheduling

📡 Real-time streaming ingestion

🤖 Automated fraud alerting system

👩‍💻 Author

Portfolio project built to demonstrate Data Engineering and Analytics capabilities in a financial domain setting.
