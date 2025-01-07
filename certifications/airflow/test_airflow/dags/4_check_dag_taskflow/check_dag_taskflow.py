from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    "retries": 3,
}


@dag(
    "4_check_dag_taskflow",
    start_date=datetime(2023, 1, 1),
    default_args=default_args,
    description="DAG to check data",
    tags=["data_engineering"],
    schedule="@daily",
    catchup=False,
)
def check_dag_taskflow():

    create_file = BashOperator(
        task_id="create_file", bash_command="scripts/create_file.sh"
    )
    check_file = BashOperator(
        task_id="check_file", bash_command="scripts/check_file.sh"
    )
    read_file = PythonOperator(
        task_id="read_file",
        python_callable=lambda: print(open("/tmp/dummy2", "rb").read()),
    )

    create_file >> check_file >> read_file


check_dag_taskflow()
