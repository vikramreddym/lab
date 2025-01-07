from datetime import datetime

from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor


@dag(
    "13b_parallel_sensor",
    schedule=None,
    start_date=datetime(2023, 1, 1),
    tags=["sensor"],
    catchup=False,
)
def second_dag():

    @task
    def runme():
        print("Hi")

    runme()


second_dag()
