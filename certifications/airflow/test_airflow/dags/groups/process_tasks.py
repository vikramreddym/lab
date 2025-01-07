from airflow.decorators import task
from airflow.utils.task_group import TaskGroup


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


@task.python
def check_a():
    print("checking")


@task.python
def check_b():
    print("checking")


@task.python
def check_c():
    print("checking")


def create_test_tasks():
    with TaskGroup("test_tasks") as test_tasks:
        check_a()
        check_b()
        check_c()
    return test_tasks


def process_tasks(partner_settings):
    with TaskGroup("process_tasks") as p_t:
        test_tasks_group = create_test_tasks()

        (
            process_a(
                partner_settings["partner_name"], partner_settings["partner_path"]
            )
            >> test_tasks_group
        )
        (
            process_b(
                partner_settings["partner_name"], partner_settings["partner_path"]
            )
            >> test_tasks_group
        )
        (
            process_c(
                partner_settings["partner_name"], partner_settings["partner_path"]
            )
            >> test_tasks_group
        )

    return p_t
