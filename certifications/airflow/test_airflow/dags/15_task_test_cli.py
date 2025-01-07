from datetime import datetime

from airflow.decorators import dag, task
from airflow.exceptions import AirflowException


@dag("15_cli", start_date=datetime(2023, 1, 1), schedule=None, catchup=False)
def cli():

    @task
    def my_task1(val):
        print(val)
        return 42

    @task
    def my_task(val):
        raise AirflowException()
        print(val)
        return 42

    my_task(80)
    my_task1(80)


cli()
