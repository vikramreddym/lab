from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator


def _ml_task(ml_param):
    print(ml_param)


with DAG(
    "10_vars_ui",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
):
    for ml_param in Variable.get("ml_model_parameters", deserialize_json=True)["param"]:
        PythonOperator(
            task_id=f"ml_task_{ml_param}",
            python_callable=_ml_task,
            op_kwargs={"ml_param": ml_param},
        )
