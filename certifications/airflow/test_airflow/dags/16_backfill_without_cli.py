from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="16_backfill_trigger_dag",
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    tags=["backfill-trigger-cli"],
    catchup=False,
    params={"dag_id": "1_my_dag", "date_start": 20230401, "date_end": 20230405},
) as dag:

    # Use the UI to trigger a DAG run with conf to trigger a backfill, passing in start/end dates and dag_id etc:
    trigger_backfill = BashOperator(
        task_id="trigger_backfill",
        bash_command="airflow dags backfill --reset-dagruns -y -s {{ dag_run.conf['date_start'] }} -e {{ dag_run.conf['date_end'] }} {{ dag_run.conf['dag_id'] }}",
    )

    trigger_backfill
