import pandas as pd
from db_connection import engine

# 1️⃣ Load raw CSV
df = pd.read_csv("../data/transactions_raw.csv", parse_dates=["timestamp"])

print(f"Loaded {len(df)} rows from CSV")

# 2️⃣ Create dim_location
dim_location = (
    df[["location"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_location["location_id"] = dim_location.index + 1

dim_location.rename(columns={"location": "city"}, inplace=True)
dim_location = dim_location[["location_id", "city"]]

dim_location.to_sql("dim_location", engine, if_exists="append", index=False)
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

dim_merchant.to_sql("dim_merchant", engine, if_exists="append", index=False)
print("✅ dim_merchant populated")

# 4️⃣ Create dim_account
dim_account = df[["account_id"]].drop_duplicates().reset_index(drop=True)
dim_account["customer_id"] = "CUST_" + (dim_account.index + 1).astype(str)
dim_account["account_type"] = "Checking"

# 5️⃣ Create dim_customer
dim_customer = dim_account[["customer_id"]].drop_duplicates()
dim_customer["customer_name"] = "Customer_" + dim_customer.index.astype(str)

dim_customer.to_sql("dim_customer", engine, if_exists="append", index=False)
print("✅ dim_customer populated")

dim_account.to_sql("dim_account", engine, if_exists="append", index=False)
print("✅ dim_account populated")


# 6️⃣ Create fact_transactions
fact = (
    df
    .merge(dim_merchant[["merchant_id", "merchant_name"]],
           left_on="merchant",
           right_on="merchant_name")
)

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

fact_table.to_sql("fact_transactions", engine, if_exists="append", index=False)
print("✅ fact_transactions populated")

print("🎉 ALL TABLES SUCCESSFULLY POPULATED")
