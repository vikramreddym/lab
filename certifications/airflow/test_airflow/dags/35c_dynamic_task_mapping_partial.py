import random
from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="35c_dynamic_task_mapping_partial",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    @task
    def get_files():
        return [f"file_{nb}" for nb in range(1, random.randint(3, 5))]

    @task.python
    def download_files(folder: str, file: str):
        print(f"Downloading {folder}/{file}")

    files = download_files.partial(folder="s3_bucket_name").expand(file=get_files())
