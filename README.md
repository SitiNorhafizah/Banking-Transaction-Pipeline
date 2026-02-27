1) Overview

This project builds a production-style data warehouse for banking transactions using PostgreSQL and Python ETL processes. It transforms raw transaction data into a structured star schema optimized for analytics and fraud detection.

2) Architecture
→ Raw CSV
→ ETL (Pandas + SQLAlchemy)
→ PostgreSQL Data Warehouse
→ Star Schema (Fact + Dimensions)
→ Analytics & Fraud Detection

3) Tech Stack
→ Python
→ PostgreSQL
→ Pandas
→ SQLAlchemy
→ Streamlit (dashboard)
→ Faker (data generation)

4) Data Model
→ Fact Table: fact_transactions

→ Dimension Tables: *dim_customer
                    *dim_account
										*dim_merchant
										*dim_location
										
→ Key Features: *Star schema modeling
                *Foreign key enforcement
								*Idempotent ETL design
								*Deduplication handling
								*Fraud flag logic
								*Data integrity constraints

5) How to Run
pip install -r requirements.txt
python etl/load_from_csv.py
