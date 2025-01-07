from datetime import datetime, timedelta

from airflow.decorators import dag, task

# from typing import Dict --> Use this instead of multiple_outputs like so: def extract() -> Dict[str, str]:


@task.python(task_id="extract_parameters", do_xcom_push=False, multiple_outputs=True)
def extract():
    return {"partner_name": "netflix", "partner_path": "/partners/netflix"}


@task.python
def process(partner_name):
    print(partner_name)


@task.python
def process_separately(partner_name, end_date):
    print(partner_name)
    print(end_date)


@dag(
    "18_xcoms_multi_params",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
)
def xcoms_multi_param():
    partner_settings = extract()
    process(partner_settings)
    process_separately(
        partner_settings["partner_name"], partner_settings["partner_path"]
    )


xcoms_multi_param()
