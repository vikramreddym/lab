from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup

default_args = {"start_date": datetime(2023, 1, 1)}


@task.python(task_id="extract_parameters", multiple_outputs=True)
def extract():
    return {"partner_name": "netflix", "partner_path": "/partners/netflix"}


@task.python
def process_a(partner_name, partner_path):
    print(partner_name)
    print(partner_path)


@task.python
def process_b(partner_name, partner_path):
    print(partner_name)
    print(partner_path)


@task.python
def process_c(partner_name, partner_path):
    print(partner_name)
    print(partner_path)


@dag(
    "20a_taskgroups",
    default_args=default_args,
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
)
def taskgroup_demo():
    partner_settings = extract()

    with TaskGroup("process_tasks") as p_t:
        process_a(partner_settings["partner_name"], partner_settings["partner_path"])
        process_b(partner_settings["partner_name"], partner_settings["partner_path"])
        process_c(partner_settings["partner_name"], partner_settings["partner_path"])


taskgroup_demo()
