from datetime import datetime

from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor


@dag(
    "13a_parallel_sensor",
    schedule=None,
    start_date=datetime(2021, 12, 1),
    tags=["sensor"],
    catchup=False,
)
def first_dag():
    wait_for_files = FileSensor.partial(
        task_id="wait_for_files", fs_conn_id="fs_default", mode="reschedule"
    ).expand(filepath=["data_1.csv", "data_2.csv", "data_3.csv"])

    @task
    def process_file():
        print("I processed the file!")

    wait_for_files >> process_file()


first_dag()
