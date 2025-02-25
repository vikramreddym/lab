from datetime import datetime

from airflow import DAG
from airflow.decorators import task

partners = {
    "snowflake": {"schedule": "@daily", "path": "/data/snowflake"},
    "netflix": {"schedule": "@weekly", "path": "/data/netflix"},
}


def generate_dag(dag_id, schedule_interval, details, default_args):
    with DAG(
        dag_id=dag_id,
        schedule_interval=schedule_interval,
        catchup=False,
        default_args=default_args,
    ) as dag:

        @task.python
        def process(path):
            print(f"Processing data from {path}")

        process(details["path"])
    return dag


for partner, details in partners.items():
    dag_id = f"dag_{partner}"
    default_args = {
        "start_date": datetime(2023, 1, 1),
    }
    globals()[dag_id] = generate_dag(dag_id, details["schedule"], details, default_args)
