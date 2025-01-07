import time
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.exceptions import AirflowSensorTimeout, AirflowTaskTimeout
from airflow.operators.empty import EmptyOperator
from groups.process_tasks_taskflow import process_tasks

partners = {
    "partner_snowflake": {
        "name": "snowflake",
        "path": "/partners/snowflake",
        "priority": 2,
        "pool": "snowflake",
    },
    "partner_netflix": {
        "name": "netflix",
        "path": "/partners/netflix",
        "priority": 3,
        "pool": "netflix",
    },
    "partner_astronomer": {
        "name": "astronomer",
        "path": "/partners/astronomer",
        "priority": 4,
        "pool": "astronomer",
    },
}
default_args = {"start_date": datetime(2023, 1, 1)}


def _success_callback(context):
    print("Success callback")


def _failure_callback(context):
    print("Failure callback")


def _extract_callback_success(context):
    print("Success callback extract")


def _extract_callback_failure(context):
    print("Failure callback extract")
    if (context["exception"]) is not None:
        if (isinstance(context["exception"], AirflowTaskTimeout)) or (
            isinstance(context["exception"], AirflowSensorTimeout)
        ):
            print("Failed because of timeout")


def _extract_callback_retry(context):
    print("Retry callback extract")
    if (context["ti"]._try_number) > 2:
        print("number of retries exceeded")


@dag(
    "30_callbacks",
    default_args=default_args,
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
    max_active_runs=1,
    on_failure_callback=_failure_callback,
    on_success_callback=_success_callback,
)
def my_dag():
    start = EmptyOperator(task_id="start")
    storing = EmptyOperator(task_id="storing", trigger_rule="none_failed_or_skipped")

    for partner, details in partners.items():

        @task.python(
            task_id=f"extract_{partner}",
            multiple_outputs=True,
            pool=details["pool"],
            priority_weight=details["priority"],
            depends_on_past=True,
            on_failure_callback=_extract_callback_failure,
            on_success_callback=_extract_callback_success,
            on_retry_callback=_extract_callback_retry,
        )
        def extract(partner_name, partner_path):
            time.sleep(5)
            return {"partner_name": partner_name, "partner_path": partner_path}

        extract_partner = extract(details["name"], details["path"])
        start >> extract_partner
        process_tasks(extract_partner) >> storing


my_dag()
