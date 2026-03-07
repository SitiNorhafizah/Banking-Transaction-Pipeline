# ml/score_model.py
import pandas as pd
from sqlalchemy import create_engine, text
import joblib
import os

# Load environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Connect to PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load trained model
model = joblib.load("model.pkl")

# Fetch new transactions (fraud_score = 0 means not scored yet)
query = """
SELECT * FROM fact_transactions
WHERE fraud_score = 0
"""
df = pd.read_sql(query, engine)

if df.empty:
    print("No new transactions to score")
else:
    # Feature engineering
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    features = ["amount", "hour", "day_of_week"]
    X = df[features]

    # Predict fraud
    df["fraud_flag"] = model.predict(X).astype(bool)
    df["fraud_score"] = model.predict_proba(X)[:, 1]

    # Update database
    with engine.begin() as conn:
        for _, row in df.iterrows():
            update_query = text("""
                UPDATE fact_transactions
                SET fraud_flag = :fraud_flag,
                    fraud_score = :fraud_score
                WHERE transaction_id = :transaction_id
            """)
            conn.execute(update_query, {
                "fraud_flag": row["fraud_flag"],
                "fraud_score": row["fraud_score"],
                "transaction_id": row["transaction_id"]
            })

    print(f"Scored {len(df)} transactions")
