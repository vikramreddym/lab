# test_module.py


import pendulum
from airflow.decorators import dag, task
from my_packages.package_a.module_a import TestClass


@dag(
    "12_test_module",
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 1),
    catchup=False,
)
def test_module():
    @task
    def test_task():
        print(TestClass.my_time())

    test_task()


test_module()
