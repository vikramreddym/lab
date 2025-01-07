from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.subdag import SubDagOperator
from subdag.subdag_factory import subdag_factory

default_args = {"start_date": datetime(2023, 1, 1)}


@task.python(task_id="extract_parameters", multiple_outputs=True)
def extract():
    return {"partner_name": "netflix", "partner_path": "/partners/netflix"}


@dag(
    "19_parent_dag",
    default_args=default_args,
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
)
def parent_dag():
    partner_settings = extract()
    process_tasks = SubDagOperator(
        task_id="process_tasks",
        subdag=subdag_factory("19_parent_dag", "process_tasks", default_args),
    )

    partner_settings >> process_tasks


parent_dag()
