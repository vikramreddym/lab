from datetime import datetime

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator


def print_a():
    print("hi from task a")


def print_b():
    print("hi from task b")


def print_c():
    print("hi from task c")


def print_d():
    print("hi from task d")


def print_e():
    print("hi from task e")


default_args = {
    "retries": 3,
}

with DAG(
    "1_my_dag",
    start_date=datetime(2020, 1, 1),
    default_args=default_args,
    description="A simple tutorial DAG",
    tags=["data_science"],
    schedule="@daily",
    catchup=False,
):
    task_a = PythonOperator(task_id="task_a", python_callable=print_a)
    task_b = PythonOperator(task_id="task_b", python_callable=print_b)
    task_c = PythonOperator(task_id="task_c", python_callable=print_c)
    task_d = PythonOperator(task_id="task_d", python_callable=print_d)
    task_e = PythonOperator(task_id="task_e", python_callable=print_e)

    # task_a >> [task_b, task_c, task_d] >> task_e
    chain(task_a, [task_b, task_c], [task_d, task_e])
