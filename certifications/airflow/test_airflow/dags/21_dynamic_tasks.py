from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from groups.process_tasks_taskflow import process_tasks

partners = {
    "partner_snowflake": {"name": "snowflake", "path": "/partners/snowflake"},
    "partner_netflix": {"name": "netflix", "path": "/partners/netflix"},
    "partner_astronomer": {"name": "astronomer", "path": "/partners/astronomer"},
}


@dag(
    "21_dynamic_tasks",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    tags=["dynamic"],
    catchup=False,
)
def dynamic_tasks():
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    for partner, details in partners.items():

        @task.python(task_id=f"extract_{partner}", multiple_outputs=True)
        def extract(partner_name, partner_path):
            return {"partner_name": partner_name, "partner_path": partner_path}

        extract_partner = extract(details["name"], details["path"])
        process_task = process_tasks(extract_partner)

        start >> extract_partner >> process_task >> end


dynamic_tasks()
