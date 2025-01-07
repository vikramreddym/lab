import time
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.sensors.date_time import DateTimeSensor
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


@dag(
    "29_datetime_sensor",
    default_args=default_args,
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
    max_active_runs=1,
)
def my_dag():
    start = EmptyOperator(task_id="start")
    storing = EmptyOperator(task_id="storing", trigger_rule="none_failed_or_skipped")

    delay = DateTimeSensor(
        task_id="delay",
        target_time="{{ execution_date.add(minutes=10) }}",
        poke_interval=10 * 60,
        mode="reschedule",
        timeout=11 * 60,
        soft_fail=True,
        exponential_backoff=True,
    )

    for partner, details in partners.items():

        @task.python(
            task_id=f"extract_{partner}",
            multiple_outputs=True,
            pool=details["pool"],
            priority_weight=details["priority"],
            depends_on_past=True,
        )
        def extract(partner_name, partner_path):
            time.sleep(5)
            return {"partner_name": partner_name, "partner_path": partner_path}

        extract_partner = extract(details["name"], details["path"])
        start >> delay >> extract_partner
        process_tasks(extract_partner) >> storing


my_dag()
