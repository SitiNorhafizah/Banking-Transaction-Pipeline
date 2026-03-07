from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "fiza",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="banking_etl_pipeline",
    default_args=default_args,
    description="Run banking ETL pipeline",
    schedule_interval="@daily",  # change to "@hourly" if you want
    start_date=datetime(2026, 3, 3),
    catchup=False,
) as dag:

    run_etl = BashOperator(
        task_id="run_etl_script",
        bash_command="python /app/etl/load_from_csv.py"
    )

    run_etl
