from airflow.decorators import task, task_group


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


@task_group
def test_tasks():
    check_a()
    check_b()
    check_c()


@task_group(group_id="process_tasks")
def process_tasks(partner_settings):
    # Create task dependencies
    test_task_group = test_tasks()

    (
        process_a(partner_settings["partner_name"], partner_settings["partner_path"])
        >> test_task_group
    )

    (
        process_b(partner_settings["partner_name"], partner_settings["partner_path"])
        >> test_task_group
    )

    (
        process_c(partner_settings["partner_name"], partner_settings["partner_path"])
        >> test_task_group
    )
