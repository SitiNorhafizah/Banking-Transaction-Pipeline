import pandas as pd
from db_connection import engine
import time
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import OperationalError
import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Wait for database to be ready
for i in range(10):
    try:
        with engine.connect() as conn:
            print("Database is ready.")
            break
    except OperationalError:
        print("Waiting for database...")
        time.sleep(3)
else:
    raise Exception("Database not available after waiting.")

# 1️⃣ Load raw CSV
df = pd.read_csv("../data/transactions_raw.csv", parse_dates=["timestamp"])
print(f"Loaded {len(df)} rows from CSV")

# 2️⃣ Create dim_location
dim_location = df[["location"]].drop_duplicates().reset_index(drop=True)
dim_location["location_id"] = dim_location.index + 1
dim_location.rename(columns={"location": "city"}, inplace=True)
dim_location = dim_location[["location_id", "city"]]

dim_location.to_sql("dim_location", engine, if_exists="append", index=False, method='multi')
print("✅ dim_location populated")

# 3️⃣ Create dim_merchant
dim_merchant = (
    df[["merchant", "location"]]
    .drop_duplicates()
    .merge(dim_location, left_on="location", right_on="city")
)
dim_merchant = dim_merchant.reset_index(drop=True)
dim_merchant["merchant_id"] = dim_merchant.index + 1
dim_merchant.rename(columns={"merchant": "merchant_name"}, inplace=True)
dim_merchant = dim_merchant[["merchant_id", "merchant_name", "location_id"]]

dim_merchant.to_sql("dim_merchant", engine, if_exists="append", index=False, method='multi')
print("✅ dim_merchant populated")

# 4️⃣ Create dim_account
dim_account = df[["account_id"]].drop_duplicates().reset_index(drop=True)
dim_account["customer_id"] = "CUST_" + (dim_account.index + 1).astype(str)
dim_account["account_type"] = "Checking"

# 5️⃣ Create dim_customer
dim_customer = dim_account[["customer_id"]].drop_duplicates()
dim_customer["customer_name"] = "Customer_" + dim_customer.index.astype(str)

dim_customer.to_sql("dim_customer", engine, if_exists="append", index=False, method='multi')
print("✅ dim_customer populated")

dim_account.to_sql("dim_account", engine, if_exists="append", index=False, method='multi')
print("✅ dim_account populated")

# 6️⃣ Create fact_transactions (UPSERT to avoid duplicates)
fact = df.merge(dim_merchant[["merchant_id", "merchant_name"]],
                left_on="merchant",
                right_on="merchant_name")
fact["fraud_flag"] = False

fact_table = fact[[
    "transaction_id",
    "account_id",
    "merchant_id",
    "amount",
    "timestamp",
    "fraud_flag"
]]

fact_table = fact_table.drop_duplicates(subset=["transaction_id"])

# UPSERT loop to avoid primary key conflicts
with engine.begin() as conn:
    for _, row in fact_table.iterrows():
        conn.execute(text("""
            INSERT INTO fact_transactions
            (transaction_id, account_id, merchant_id, amount, timestamp, fraud_flag)
            VALUES (:transaction_id, :account_id, :merchant_id, :amount, :timestamp, :fraud_flag)
            ON CONFLICT (transaction_id) DO NOTHING
        """), {
            "transaction_id": row["transaction_id"],
            "account_id": row["account_id"],
            "merchant_id": row["merchant_id"],
            "amount": row["amount"],
            "timestamp": row["timestamp"],
            "fraud_flag": row["fraud_flag"]
        })

print("✅ fact_transactions populated (duplicates skipped)")

print("🎉 ALL TABLES SUCCESSFULLY POPULATED")
