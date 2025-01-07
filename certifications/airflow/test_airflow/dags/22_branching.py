from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from groups.process_tasks_taskflow import process_tasks

partners = {
    "partner_snowflake": {"name": "snowflake", "path": "/partners/snowflake"},
    "partner_netflix": {"name": "netflix", "path": "/partners/netflix"},
    "partner_astronomer": {"name": "astronomer", "path": "/partners/astronomer"},
}
default_args = {"start_date": datetime(2023, 1, 1)}


def _choose_partner_based_on_day(execution_date):
    day = execution_date.day_of_week
    print(type(execution_date))
    print("execution_date: ", execution_date)
    print("day from choose_partner: ", day)
    if day == 1:
        return "extract_partner_snowflake"
    elif day == 3:
        return "extract_partner_netflix"
    elif day == 5:
        return "extract_partner_astronomer"
    return "stop"


@dag(
    "22_branching",
    default_args=default_args,
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
    max_active_runs=1,
)
def my_dag():
    start = EmptyOperator(task_id="start")
    choose_partner = BranchPythonOperator(
        task_id="choose_partner", python_callable=_choose_partner_based_on_day
    )

    stop = EmptyOperator(task_id="stop")

    choose_partner >> stop

    for partner, details in partners.items():

        @task.python(task_id=f"extract_{partner}", multiple_outputs=True)
        def extract(partner_name, partner_path):
            return {"partner_name": partner_name, "partner_path": partner_path}

        extract_partner = extract(details["name"], details["path"])
        start >> choose_partner >> extract_partner
        process_tasks(extract_partner)


my_dag()
