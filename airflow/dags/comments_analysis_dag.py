from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator

from .stream_ytb_comments import stream_ytb_comments

with DAG(dag_id='comments_analysis', schedule_interval='@daily', catchup=False):
    stream_ytb_comments_task = PythonOperator(
        task_id='stream_ytm_comments',
        python_callable=stream_ytb_comments
    )
