import time
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from groups.process_tasks_taskflow import process_tasks

partners = {
    "partner_snowflake": {"name": "snowflake", "path": "/partners/snowflake"},
    "partner_netflix": {"name": "netflix", "path": "/partners/netflix"},
    "partner_astronomer": {"name": "astronomer", "path": "/partners/astronomer"},
}
default_args = {"start_date": datetime(2023, 1, 1)}


@dag(
    "34_xcoms_dag",
    default_args=default_args,
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
)
def my_dag():
    start = EmptyOperator(task_id="start")
    storing = EmptyOperator(task_id="storing", trigger_rule="none_failed_or_skipped")

    for partner, details in partners.items():

        @task.python(task_id=f"extract_{partner}", multiple_outputs=True)
        def extract(partner_name, partner_path):
            time.sleep(5)
            return {"partner_name": partner_name, "partner_path": partner_path}

        extract_partner = extract(details["name"], details["path"])
        start >> extract_partner
        process_tasks(extract_partner) >> storing


my_dag()
