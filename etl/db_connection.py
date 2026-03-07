# ml/score_model.py
import os
import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# 1️⃣ Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")  # Note: match your .env variable
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

# 2️⃣ Create SQLAlchemy engine
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# 3️⃣ Wait for database to be ready
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

# 4️⃣ Query transactions
query = text("SELECT * FROM fact_transactions LIMIT 100")  # example query
df = pd.read_sql(query, engine)
print(f"Loaded {len(df)} transactions from DB")

# 5️⃣ Example: ML scoring placeholder
# Replace this with your actual ML model loading & prediction
df["fraud_score"] = 0.1  # dummy score for testing
print(df.head())
