from datetime import datetime

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain, cross_downstream

default_args = {"retries": 3}


@dag(
    "24_chain_cross_downstream",
    start_date=datetime(2020, 12, 31),
    default_args=default_args,
    description="My Dag TaskFlow",
    tags=["data_science"],
    schedule="@daily",
    catchup=False,
)
def my_dag_taskflow():

    @task
    def start():
        print("Hi from task start")

    @task
    def print_a():
        print("Hi from task a")

    @task
    def print_b():
        print("Hi from task b")

    @task
    def print_c():

        print("Hi from task c")

    @task
    def print_d():
        print("Hi from task d")

    @task
    def print_e():
        print("Hi from task e")

    @task
    def print_f():
        print("Hi from task f")

    @task
    def end():
        print("Hi from task end")

    x = [print_a(), print_b(), print_c()]
    y = [print_d(), print_e(), print_f()]

    chain(start(), x, y, end())
    cross_downstream(x, y)


my_dag_taskflow()
