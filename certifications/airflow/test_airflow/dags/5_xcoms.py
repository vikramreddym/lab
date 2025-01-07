import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator


def _transform(ti):
    import requests

    resp = requests.get("https://swapi.dev/api/people/1").json()
    print(resp)

    my_character = {}
    my_character["height"] = int(resp["height"]) - 20
    my_character["mass"] = int(resp["mass"]) - 50
    my_character["hair_color"] = "black" if resp["hair_color"] == "blond" else "blond"
    my_character["eye_color"] = "hazel" if resp["eye_color"] == "blue" else "blue"
    my_character["gender"] = "female" if resp["gender"] == "male" else "female"
    ti.xcom_push("character_info", my_character)


def _load(ti):
    print(ti.xcom_pull(key="character_info", task_ids="transform"))


with DAG(
    "5_xcom_demo",
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 1),
    catchup=False,
):

    transform = PythonOperator(task_id="transform", python_callable=_transform)

    load = PythonOperator(task_id="load", python_callable=_load)

    transform >> load
