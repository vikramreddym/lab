from datetime import datetime

from airflow.decorators import dag, task
from airflow.providers.http.hooks.http import HttpHook
from airflow.sensors.base import PokeReturnValue


@dag(
    "14_sensor_decorator",
    schedule=None,
    start_date=datetime(2021, 12, 1),
    catchup=False,
)
def sensor_decorator():

    @task.sensor(poke_interval=30, timeout=120, mode="poke")
    def check_api_availability() -> PokeReturnValue:
        conn_id = "calendar_api"
        http_hook = HttpHook(method="GET", http_conn_id=conn_id)
        connection = http_hook.get_connection(conn_id)
        api_key = connection.extra_dejson.get("api_key")
        query_params = {
            "api_key": api_key,
            "country": "jghv",
            "year": 2019,
        }
        try:
            r = http_hook.run(endpoint="holidays", data=query_params)
            if r.status_code == 200:
                print("API is available")
                json_data = r.json()
                print("API response", json_data)
                return PokeReturnValue(is_done=True, xcom_value=json_data)
            else:
                print(f"API returned status code {r.status_code}")
        except Exception as e:
            print(f"API request failed {e}")

        return PokeReturnValue(is_done=False, xcom_value=None)

    @task()
    def process_api_response(api_response):
        print("API response", api_response)

    api_response = check_api_availability()
    process_api_response(api_response)


sensor_decorator()
