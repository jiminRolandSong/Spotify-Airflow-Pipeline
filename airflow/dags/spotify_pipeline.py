from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/home/aangava/MSP/scripts')

try:
    from extract_spotify import main as extract_main
    from transform_spotify import main as transform_main
    from load_spotify import main as load_main
except ImportError as e:
    print(f"Import error: {e}")
    raise

default_args = {
    'owner': 'aanga',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'spotify_pipeline',
    default_args=default_args,
    description='ETL pipeline for Spotify data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 4, 17),
    catchup=False,
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_spotify_data',
        python_callable=extract_main,
    )
    
    transform_task = PythonOperator(
        task_id='transform_spotify_data',
        python_callable=transform_main,
    )
    
    load_task = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_main,
    )
    
    extract_task >> transform_task >> load_task