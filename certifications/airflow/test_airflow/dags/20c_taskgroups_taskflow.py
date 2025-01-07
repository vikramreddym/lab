from datetime import datetime, timedelta

from airflow.decorators import dag, task
from groups.process_tasks_taskflow import process_tasks

default_args = {"start_date": datetime(2023, 1, 1)}


@task.python(task_id="extract_parameters", multiple_outputs=True)
def extract():
    return {"partner_name": "netflix", "partner_path": "/partners/netflix"}


@dag(
    "20c_taskgroups_external_taskflow",
    default_args=default_args,
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
)
def taskgroup_demo():
    partner_settings = extract()
    tasks = process_tasks(partner_settings)

    @task
    def result():
        print("Processing completed")

    partner_settings >> tasks >> result()


taskgroup_demo()
