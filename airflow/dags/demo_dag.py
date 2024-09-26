import os
from datetime import datetime
from airflow.models.dag import DAG
from airflow.models import Variable
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

    @task
    def print_env_var():
        kafka_topic = os.environ.get('COMMENTS_TOPIC_NAME')
        api_key = os.environ.get('GOOGLE_API_KEY')
        print(f"{kafka_topic=}")
        print(f"{api_key=}")

    set_env_var = BashOperator(task_id='set_env_var',
                               bash_command='export AIRFLOW_VAR_COMMENTS_TOPIC_NAME=$COMMENTS_TOPIC_NAME ' \
                               '&& echo AIRFLOW_VAR_COMMENTS_TOPIC_NAME=$AIRFLOW_VAR_COMMENTS_TOPIC_NAME ' \
                               '&& export AIRFLOW_VAR_GOOGLE_API_KEY=$GOOGLE_API_KEY ' \
                               '&& echo AIRFLOW_VAR_GOOGLE_API_KEY=$AIRFLOW_VAR_GOOGLE_API_KEY')

    @task
    def print_context_var():
        kafka_topic = Variable.get('comments_topic_name')
        api_key = "KEY" # Variable.get('google_api_key')
        print(f"{kafka_topic=}")
        print(f"{api_key=}")

    # Set dependencies between tasks
    hello >> print_world()
    hello >> print_rochdy()
    hello >> print_airflow()
    hello >> airflow()
    set_env_var >> print_context_var()
    print_env_var()
