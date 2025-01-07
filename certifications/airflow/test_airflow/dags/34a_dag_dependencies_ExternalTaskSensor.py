from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.external_task import ExternalTaskSensor

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    dag_id="34a_dag_dependencies_ExternalTaskSensor_cleaning_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    wait_for_storing_xcoms = ExternalTaskSensor(
        task_id="wait_for_cleaning_xcoms",
        external_dag_id="34_xcoms_dag",
        external_task_id="storing",
    )

    cleaning_xcoms = PostgresOperator(
        task_id="cleaning_xcoms",
        sql="sql/cleaning_xcoms.sql",
        postgres_conn_id="postgres",
    )

    wait_for_storing_xcoms >> cleaning_xcoms
