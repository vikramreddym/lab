from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="35a_dynamic_task_mapping",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    @task.python
    def download_files(file: str):
        print(f"Downloading {file}")

    files = download_files.expand(file=["file1.csv", "file2.csv", "file3.csv"])
