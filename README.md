# 🏦 Banking Transaction ETL & Fraud Analytics Platform

An end-to-end Data Engineering & Analytics project simulating a banking transaction system with:

- PostgreSQL data warehouse (Star Schema)
- Production-style ETL pipeline
- Interactive Streamlit fraud analytics dashboard
- ML-based risk scoring & downloadable reports

---

## 🚀 Project Objective

Simulate a real-world banking environment where raw transaction data is:

1. Extracted from CSV files  
2. Transformed into dimensional models  
3. Loaded into a PostgreSQL data warehouse  
4. Visualized through an interactive Streamlit dashboard

Supports fraud detection, risk scoring, and filtered reporting for stakeholders.

---

## 🏗 System Architecture


Raw CSV
↓
Python ETL (Pandas + SQLAlchemy)
↓
PostgreSQL Data Warehouse (Star Schema)
↓
Streamlit Dashboard (Interactive Analytics)


---

## 🧱 Data Warehouse Design

**Star Schema**  

**Dimension Tables:** `dim_customer`, `dim_account`, `dim_merchant`, `dim_location`  
**Fact Table:** `fact_transactions` (transaction_id, account_id, merchant_id, amount, timestamp, fraud_flag, fraud_score)

**ETL Guarantees:**
- ✅ Idempotent loads (no duplicate inserts)  
- ✅ Referential integrity  
- ✅ Clean dimensional modeling  
- ✅ Structured transformation logic

---

## 📊 Dashboard Features

Built with Streamlit + Plotly  

**Key Metrics (KPIs):** Total Transactions, Total Amount, Fraud Cases, Max & Avg Fraud Score  
**Daily Transaction Volume:** Interactive line chart  
**Fraud Alerts:** High-risk transactions flagged  
**Top Risky Accounts & Merchants:** Avg fraud score by account/merchant  
**Filters:** Account ID, Merchant, Location, Date Range  
**Downloadable Reports:** Export filtered transactions as CSV

---

## 🤖 Machine Learning Integration

- Fraud prediction model trained on historical transactions  
- Generates `fraud_score` for new transactions  
- Highlights high-risk transactions in the dashboard

---

## 🛠 Tech Stack

- **Backend / ETL:** Python, Pandas, SQLAlchemy  
- **Database:** PostgreSQL  
- **Visualization:** Streamlit, Plotly  
- **Environment:** Virtual Environment (venv)  

---

## 📂 Repository Structure


Banking-Transaction-Pipeline/
│
├── data/ # Raw transaction CSV
├── etl/ # ETL scripts
│ ├── load_from_csv.py
│ ├── etl_phase2.py
│ └── reset.py
├── ml/ # ML training & scoring
│ ├── train_model.py
│ └── score_model.py
├── dashboard/
│ └── app.py
├── requirements.txt
├── .gitignore
└── README.md


---

## ⚙ How to Run Locally

1️⃣ **Create Virtual Environment**

```bash
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
🔮 Future Enhancements

🐳 Docker containerization

⏰ Apache Airflow DAG scheduling

📡 Real-time streaming ingestion

🚨 Automated fraud alerting system

🔐 Environment Variables

Create a .env file in the root:

DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banking_dw
🎯 Skills Demonstrated

Data Warehouse Modeling (Star Schema)

ETL Pipeline Design

Incremental & Idempotent Loading

SQL Joins & Foreign Keys

Data Validation

Fraud Risk Scoring Logic

Interactive Dashboard Development

Production-style Project Structure

👩‍💻 Author

Portfolio project built to demonstrate Data Engineering and Analytics capabilities in a financial domain setting.
