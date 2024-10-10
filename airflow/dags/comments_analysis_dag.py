from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.models.param import Param
from datetime import datetime, timedelta
from stream_ytb_comments import stream_ytb_comments
from update_last_comments_analysis_timestamp import update_last_comments_analysis_timestamp

# Default arguments for the DAG
DAG_DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

# Define comments analysis DAG
with DAG(
    dag_id = 'comments_analysis',
    params = {
        "video_id": Param(
            type="string",
        ),
    },
    render_template_as_native_obj=True, # provide params to Tasks as specified type instead of (default behavior) string
    default_args = DAG_DEFAULT_ARGS,
    schedule_interval = None,
    start_date = datetime.today(),
    catchup = False
) as dag:
    # Define data streaming task
    stream_ytb_comments_task = PythonOperator(
        task_id='stream_ytb_comments',
        python_callable=stream_ytb_comments
    )
    # Define timestamp updating task
    update_last_comments_analysis_timestamp_task = PythonOperator(
        task_id='update_last_comments_analysis_timestamp',
        python_callable=update_last_comments_analysis_timestamp,
        op_args={
            "{{ params.video_id }}",
        }
    )
    # Define tasks' dependency
    stream_ytb_comments_task >> update_last_comments_analysis_timestamp_task

if __name__ == '__main__':
    dag.test()