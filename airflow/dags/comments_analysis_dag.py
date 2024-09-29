from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from stream_ytb_comments import stream_ytb_comments

# Default arguments for the DAG
DAG_DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

# Define comments analysis DAG
with DAG(
    dag_id = 'comments_analysis',
    default_args = DAG_DEFAULT_ARGS,
    schedule_interval = '@daily',
    start_date = datetime.today(),
    catchup = False
) as dag:
    # Define data streaming task
    stream_ytb_comments_task = PythonOperator(
        task_id='stream_ytb_comments',
        python_callable=stream_ytb_comments
    )

if __name__ == '__main__':
    dag.test()