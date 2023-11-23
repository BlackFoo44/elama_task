from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
import pendulum
import os
from add_data import load_csv_to_postgres, create_materialized, upload_to_bigquery
from pathlib import Path

ROOT_DIR = str(Path(__file__).resolve().parents[1])

# Пути к CSV файлам
webinar_csv = os.path.join(ROOT_DIR, 'dags', 'scv_files', 'webinar.csv')
users_csv = os.path.join(ROOT_DIR, 'dags', 'scv_files', 'users.csv')
transactions_csv = os.path.join(ROOT_DIR, 'dags', 'scv_files', 'transactions.csv')
name_for_materializer = 'test_1'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 4,
    'schedule_interval': None,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
        'test_task',
        default_args=default_args,
        description='test_task ETL DAG',
        schedule_interval="0 0 * * *",
        start_date=pendulum.today('UTC').add(days=-1),
        tags=['test_task'],
        max_active_runs=1
) as dag:
    load_webinar = PythonOperator(
        task_id='load_webinar',
        python_callable=load_csv_to_postgres,
        op_kwargs={'table_name': 'webinar', 'csv_file': webinar_csv},
        dag=dag,
    )

    load_users = PythonOperator(
        task_id='load_users',
        python_callable=load_csv_to_postgres,
        op_kwargs={'table_name': 'users', 'csv_file': users_csv},
        dag=dag,
    )

    load_transactions = PythonOperator(
        task_id='load_transactions',
        python_callable=load_csv_to_postgres,
        op_kwargs={'table_name': 'transactions', 'csv_file': transactions_csv},
        dag=dag,
    )
    load_materialized = PythonOperator(
        task_id='create_materialized',
        python_callable=create_materialized,
        op_kwargs={'name_for_materializer': name_for_materializer},
        dag=dag,
    )
    send_materialized = PythonOperator(
        task_id='upload_to_bigquery',
        python_callable=upload_to_bigquery,
        op_kwargs={'name_for_materializer': name_for_materializer, 'project_id': 'mytestproject-343412', 'dataset_id': '1234567890',
                   'table_id': 'my_table'},
        dag=dag, )

    load_webinar >> load_transactions >> load_users >> load_materialized >>send_materialized

