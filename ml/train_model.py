# ml/train_model.py

import os
import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load DB credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create DB connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load transaction data
query = """
SELECT transaction_id, amount, timestamp, fraud_flag
FROM fact_transactions
"""

df = pd.read_sql(query, engine, parse_dates=["timestamp"])

print("Loaded rows:", len(df))

# Convert fraud_flag to numeric
df["fraud_flag"] = df["fraud_flag"].map({False: 0, True: 1, "f": 0, "t": 1})

# Feature engineering
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

features = ["amount", "hour", "day_of_week"]
target = "fraud_flag"

X = df[features]
y = df[target]

print("Class distribution:")
print(y.value_counts())

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Save model
MODEL_PATH = "model.pkl"
joblib.dump(model, MODEL_PATH)

print(f"Model trained and saved to {MODEL_PATH}")
print("Model classes:", model.classes_)
