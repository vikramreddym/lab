from datetime import datetime

from airflow import DAG
from airflow.sensors.python import PythonSensor


def _condition():
    return False


with DAG(
    dag_id="13_py_sensor",
    start_date=datetime(2021, 1, 1),
    schedule="@daily",
    catchup=False,
):
    waiting_for_condition = PythonSensor(
        task_id="waiting_for_condition",
        python_callable=_condition,
        poke_interval=60,
        timeout=120,
    )
