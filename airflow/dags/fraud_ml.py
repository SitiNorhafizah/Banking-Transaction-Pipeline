from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# -------------------------------
# DATABASE CONFIG
# -------------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -------------------------------
# ML TRAINING FUNCTION
# -------------------------------
def train_fraud_model():
    # Load transactions and dimension tables
    df = pd.read_sql("""
        SELECT f.transaction_id, f.account_id, f.merchant_id, f.amount, f.fraud_flag,
               m.merchant_name, l.city AS location
        FROM fact_transactions f
        LEFT JOIN dim_merchant m ON f.merchant_id = m.merchant_id
        LEFT JOIN dim_location l ON m.location_id = l.location_id
    """, engine)

    if df.empty:
        print("No data to train on")
        return

    # -------------------------------
    # PREPROCESSING
    # -------------------------------
    df['merchant_name'] = LabelEncoder().fit_transform(df['merchant_name'])
    df['location'] = LabelEncoder().fit_transform(df['location'])

    X = df[['account_id', 'merchant_id', 'amount', 'merchant_name', 'location']]
    y = df['fraud_flag']

    # -------------------------------
    # TRAIN MODEL
    # -------------------------------
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)

    # -------------------------------
    # PREDICT FRAUD SCORE (PROBABILITY)
    # -------------------------------
    df['fraud_score'] = clf.predict_proba(X)[:, 1]  # probability of fraud

    # -------------------------------
    # UPDATE DATABASE
    # -------------------------------
    # Using SQLAlchemy to update each row
    for idx, row in df.iterrows():
        engine.execute(
            """
            UPDATE fact_transactions
            SET fraud_score = %s
            WHERE transaction_id = %s
            """,
            (row['fraud_score'], row['transaction_id'])
        )

    print("Fraud scores updated successfully.")

# -------------------------------
# DAG DEFINITION
# -------------------------------
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_fraud_scoring',
    default_args=default_args,
    description='Train ML fraud model and update fraud_score',
    schedule_interval='@hourly',  # runs every hour, adjust as needed
    catchup=False,
)

train_task = PythonOperator(
    task_id='train_fraud_model',
    python_callable=train_fraud_model,
    dag=dag,
)

train_task
