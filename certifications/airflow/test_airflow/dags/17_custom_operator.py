from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


def _extract(partner_name):
    print(partner_name)


class CustomPostgresOperator(PostgresOperator):
    template_fields = ("sql", "parameters")


with DAG(
    "17_custom_operator",
    description="DAG in charge of processing customer data",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=10),
    tags=["data_science", "customer_data"],
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=_extract,
        op_args=["{{ var.json.my_dag_partner.name }}"],
    )

    fetching_data = CustomPostgresOperator(
        task_id="fetching_data",
        sql="SELECT partner_name FROM partners WHERE date = {{ ds }}",
        parameters={
            "next_ds": "{{ next_ds }}",
            "prev_ds": "{{ prev_ds }}",
            "partner_name": "{{ var.json.my_dag_partner.name }}",
        },
    )
