# etl_phase2_final.py
import pandas as pd
from sqlalchemy import text
from db_connection import engine

# ---------- 1️⃣ Create Dimension Tables ----------
def create_dimensions():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_customer (
                customer_id VARCHAR PRIMARY KEY,
                customer_name VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_account (
                account_id VARCHAR PRIMARY KEY,
                customer_id VARCHAR REFERENCES dim_customer(customer_id),
                account_type VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_location (
                location_id SERIAL PRIMARY KEY,
                city VARCHAR UNIQUE
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_merchant (
                merchant_id SERIAL PRIMARY KEY,
                merchant_name VARCHAR,
                location_id INTEGER REFERENCES dim_location(location_id),
                UNIQUE(merchant_name, location_id)
            );
        """))
    print("✅ Dimension tables created")


# ---------- 2️⃣ Populate Dimension Tables ----------
def populate_dimensions():
    df = pd.read_sql("SELECT * FROM fact_transactions", engine)

    # --- dim_customer ---
    existing_customers = pd.read_sql("SELECT customer_id FROM dim_customer", engine)
    existing_accounts = pd.read_sql("SELECT account_id, customer_id FROM dim_account", engine)

    # Identify new customers
    new_customers = df[['account_id']].drop_duplicates()
    new_customers = new_customers.merge(existing_accounts[['account_id']], on='account_id', how='left', indicator=True)
    new_customers = new_customers[new_customers['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not new_customers.empty:
        new_customers['customer_id'] = 'CUST_' + new_customers.index.astype(str)
        new_customers['customer_name'] = 'Customer_' + new_customers.index.astype(str)
        new_customers[['customer_id','customer_name']].to_sql('dim_customer', engine, if_exists='append', index=False, method='multi')

    # --- dim_account ---
    df_accounts = df[['account_id']].drop_duplicates()
    accounts_to_insert = df_accounts.merge(existing_accounts[['account_id']], on='account_id', how='left', indicator=True)
    accounts_to_insert = accounts_to_insert[accounts_to_insert['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not accounts_to_insert.empty:
        # Map customer_id from new_customers
        accounts_to_insert = accounts_to_insert.merge(new_customers[['account_id','customer_id']], on='account_id', how='left')
        accounts_to_insert['account_type'] = 'Checking'
        accounts_to_insert[['account_id','customer_id','account_type']].to_sql('dim_account', engine, if_exists='append', index=False, method='multi')

    print("✅ Customer and Account dimensions populated")

    # --- Skip dim_merchant/dim_location if fact already uses merchant_id ---
    print("⚠️ Skipping dim_merchant/dim_location population (fact already uses merchant_id)")


# ---------- 3️⃣ Populate Fact Table ----------
def populate_fact():
    df_fact = pd.read_sql("SELECT * FROM fact_transactions", engine)

    # Only new transactions (transaction_id is PK)
    existing_txns = pd.read_sql("SELECT transaction_id FROM fact_transactions", engine)
    df_fact_new = df_fact[~df_fact['transaction_id'].isin(existing_txns['transaction_id'])]

    if df_fact_new.empty:
        print("⚠️ No new transactions to insert.")
        return

    # Merge with dimension tables to ensure referential integrity
    dim_accounts = pd.read_sql("SELECT account_id FROM dim_account", engine)
    dim_merchants = pd.read_sql("SELECT merchant_id FROM dim_merchant", engine)

    df_fact_new = df_fact_new.merge(dim_accounts, on='account_id', how='inner')
    df_fact_new = df_fact_new.merge(dim_merchants, on='merchant_id', how='inner')

    df_fact_new.to_sql('fact_transactions', engine, if_exists='append', index=False, method='multi')

    print(f"✅ {len(df_fact_new)} new transactions inserted into fact table")


# ---------- 4️⃣ Reports ----------
def run_reports():
    with engine.connect() as conn:
        print("\n--- Daily Transaction Volume ---")
        result = conn.execute(text("""
            SELECT DATE(timestamp) AS txn_date, COUNT(*) AS txn_count, SUM(amount) AS total_amount
            FROM fact_transactions
            GROUP BY DATE(timestamp)
            ORDER BY txn_date;
        """))
        for row in result:
            print(row)

        print("\n--- Suspicious Transactions ---")
        result = conn.execute(text("""
            SELECT f.transaction_id,
                   c.customer_name,
                   a.account_id,
                   f.amount,
                   f.timestamp,
                   m.merchant_name,
                   l.city
            FROM fact_transactions f
            JOIN dim_account a ON f.account_id = a.account_id
            JOIN dim_customer c ON a.customer_id = c.customer_id
            LEFT JOIN dim_merchant m ON f.merchant_id = m.merchant_id
            LEFT JOIN dim_location l ON m.location_id = l.location_id
            WHERE f.fraud_flag = TRUE
            ORDER BY f.timestamp DESC
            LIMIT 20;
        """))
        for row in result:
            print(row)

        print("\n--- Account Risk Scoring ---")
        result = conn.execute(text("""
            SELECT account_id,
                   COUNT(*) AS total_txns,
                   SUM(CASE WHEN fraud_flag THEN 1 ELSE 0 END) AS fraud_txns,
                   ROUND(100.0 * SUM(CASE WHEN fraud_flag THEN 1 ELSE 0 END) / COUNT(*), 2) AS fraud_pct
            FROM fact_transactions
            GROUP BY account_id
            ORDER BY fraud_pct DESC
            LIMIT 20;
        """))
        for row in result:
            print(row)


# ---------- 5️⃣ Main ----------
def main():
    create_dimensions()
    populate_dimensions()
    populate_fact()
    run_reports()
    print("🎉 ETL completed successfully")


if __name__ == "__main__":
    main()
