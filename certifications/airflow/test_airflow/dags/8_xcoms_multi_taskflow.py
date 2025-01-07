from datetime import datetime

from airflow.decorators import dag, task


@dag(
    "8_xcom_multi_taskflow",
    schedule=None,
    start_date=datetime(2023, 3, 1),
    catchup=False,
)
def xcom_multi_taskflow():

    @task
    def peter_task(ti):  # creates xcom with key as "return_value"
        ti.xcom_push(key="mobile_phone", value="iphone")

    @task
    def lorie_task(ti):
        ti.xcom_push(key="mobile_phone", value="galaxy")

    @task
    def bryan_task(ti):
        phones = ti.xcom_pull(task_ids=["peter_task", "lorie_task"], key="mobile_phone")
        print(list(phones))

    peter_task() >> lorie_task() >> bryan_task()


xcom_multi_taskflow()
