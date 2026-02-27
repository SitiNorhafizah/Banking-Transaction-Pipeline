# 🏦 Banking Transaction ETL & Fraud Analytics Dashboard

A complete end-to-end **ETL pipeline and interactive dashboard** for banking transactions, with fraud detection and risk scoring. Designed for portfolio showcase to demonstrate **data engineering**, **data analysis**, and **dashboard development** skills.

---

## **📌 Project Overview**

This project simulates a banking transaction system:

- **ETL pipeline**: Extracts raw transaction data from CSV, loads into a PostgreSQL data warehouse, and populates **dimension** and **fact tables**.
- **Data warehouse**: Star schema with `dim_customer`, `dim_account`, `dim_merchant`, `dim_location`, and `fact_transactions`.
- **Fraud analytics dashboard**: Built with Streamlit, showing KPIs, risk scoring, and interactive charts.

---

## **💻 Tech Stack**

- **Python** (Pandas, SQLAlchemy, Streamlit)  
- **PostgreSQL** for data warehouse  
- **Plotly** for interactive charts  
- ETL best practices: incremental loads, idempotency, FK validation

---

## **🚀 Features**

### **ETL Pipeline**
- Load CSV data into dimension and fact tables
- Idempotent insertion: repeated runs do not duplicate data
- Foreign key and data validation

### **Dashboard Features**
1. **KPIs**: Total transactions, total amount, fraud cases
2. **Fraud Risk Scoring**: Top risky accounts, merchants, and transaction types
3. **Interactive Filtering**: Filter by account, merchant, and date range
4. **Charts & Hover Info**: Clean, interactive visualizations
5. **Downloadable Reports**: Export CSV summaries for stakeholders

---

## **📂 Repository Structure**
Banking-Transaction-Pipeline/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── data/
│ └── transactions_raw.csv
│
├── etl/
│ ├── etl_phase2.py # Main ETL pipeline
│ ├── load_from_csv.py # Load CSV into DW
│ └── reset.py # Reset database tables
│
├── dashboard/
│ └── app.py # Streamlit dashboard
│
└── docs/ # Screenshots / GIFs / reports
