import random
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="35e_dynamic_task_mapping_practice",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    @task
    def get_files():
        return [f"file_{nb}" for nb in range(1, random.randint(3, 5))]

    @task.python
    def download_files(folder: str, file: str):
        return f"{folder}/{file}"

    files = download_files.partial(folder="s3_bucket_name").expand(file=get_files())

    print_files = BashOperator(
        task_id="print_files",
        bash_command="echo '{{ ti.xcom_pull(task_ids='download_files', dag_id='35e_dynamic_task_mapping_practice', key='return_value') | list }}'",
        # bash_command=""" echo '[{{ ti.xcom_pull(task_ids="download_files", dag_id="35e_dynamic_task_mapping_practice", key="return_value") | join("', '") }}]' """,
    )

    files >> print_files
