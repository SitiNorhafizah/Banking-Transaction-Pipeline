# airflow/dags/ml_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'fiza',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_etl():
    subprocess.run(["python", "/app/etl/etl_phase2.py"], check=True)

def run_ml():
    subprocess.run(["python", "/app/ml/score_model.py"], check=True)

with DAG(
    'etl_ml_pipeline',
    default_args=default_args,
    description='ETL + ML scoring pipeline',
    schedule_interval='@hourly',  # run every hour
    start_date=datetime(2026, 3, 1),
    catchup=False,
) as dag:

    etl_task = PythonOperator(
        task_id='run_etl',
        python_callable=run_etl
    )

    ml_task = PythonOperator(
        task_id='run_ml',
        python_callable=run_ml
    )

    etl_task >> ml_task  # ML runs after ETL
