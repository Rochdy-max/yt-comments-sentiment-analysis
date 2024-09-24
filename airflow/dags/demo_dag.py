from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(dag_id="demo_dag", start_date=datetime.today(), schedule="0 0 * * *") as dag:
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def print_world():
        print("world")

    @task()
    def print_rochdy():
        print("rochdy")

    @task()
    def print_airflow():
        print("airflow")

    @task()
    def airflow():
        print("airflow")

    # Set dependencies between tasks
    hello >> print_world()
    hello >> print_rochdy()
    hello >> print_airflow()
    hello >> airflow()
