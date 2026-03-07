🏦 Banking Transaction ETL & Fraud Analytics Platform

An end-to-end Data Engineering & Analytics project that simulates a banking transaction system with:

    A PostgreSQL data warehouse (Star Schema)
    A production-style ETL pipeline
    An interactive fraud analytics dashboard
    Risk scoring & downloadable reports

This project demonstrates the complete data lifecycle: ingestion → transformation → storage → analytics → visualization
🚀 Project Objective

To simulate a real-world banking environment where raw transaction data is:

    Extracted from CSV files
    Transformed into dimensional models
    Loaded into a PostgreSQL data warehouse
    Visualized through an interactive Streamlit dashboard

The system supports fraud detection, risk scoring, and filtered reporting for stakeholders.
🏗 System Architecture

Raw CSV
   ↓
Python ETL (Pandas + SQLAlchemy)
   ↓
PostgreSQL Data Warehouse (Star Schema)
   ↓
Streamlit Dashboard (Interactive Analytics)

🧱 Data Warehouse Design
Star Schema Model
Dimension Tables

    dim_customer
    dim_account
    dim_merchant
    dim_location

Fact Table

    fact_transactions
        transaction_id
        account_id
        merchant_id
        amount
        timestamp
        fraud_flag

ETL Guarantees

    ✅ Idempotent loads (no duplicate inserts)
    ✅ Referential integrity
    ✅ Clean dimensional modeling
    ✅ Structured transformation logic

📊 Dashboard Features

Built using Streamlit + Plotly
📌 Key Metrics (KPIs)

    Total Transactions
    Total Transaction Amount
    Fraud Cases

📈 Daily Transaction Volume

    Interactive line chart
    Hover tooltips
    Dynamic filtering

⚠ Fraud Risk Scoring

    Top Risky Accounts
    Top Risky Merchants
    Fraud intensity visualization

🔎 Interactive Filters

    Account ID
    Merchant
    Location
    Date Range

💾 Downloadable Reports

    Export filtered transactions as CSV

🛠 Tech Stack

Backend / ETL

    Python
    Pandas
    SQLAlchemy

Database

    PostgreSQL

Visualization

    Streamlit
    Plotly

Environment

    Virtual Environment (venv)

📂 Repository Structure

Banking-Transaction-Pipeline/
│
├── data/                  # Raw transaction CSV
├── etl/                   # ETL scripts
│   ├── load_from_csv.py
│   ├── etl_phase2.py
│   └── reset.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
├── .gitignore
└── README.md

⚙ How to Run Locally
1️⃣ Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Ensure PostgreSQL Is Running

Create database:

CREATE DATABASE banking_dw;

4️⃣ Run ETL Pipeline

python etl/load_from_csv.py

5️⃣ Launch Dashboard

streamlit run dashboard/app.py

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
    🤖 Machine Learning fraud prediction
    📡 Real-time streaming ingestion
    🚨 Automated fraud alerting system

🔐 Secrets & Configuration

Database credentials are stored in .env (ignored by Git).
Copy .env.example to .env and update values before running locally.

👩‍💻 Author

Portfolio project built to demonstrate Data Engineering and Analytics capabilities in a financial domain setting.
