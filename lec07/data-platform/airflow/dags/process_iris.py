
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.email import send_email
from datetime import timedelta
from datetime import datetime
import os
import subprocess
import logging

# Import our custom operator
from dbt_operator import DbtOperator

# Get environment variables
ANALYTICS_DB = os.getenv('ANALYTICS_DB', 'analytics')
PROJECT_DIR = os.getenv('AIRFLOW_HOME')+"/dags/dbt/homework"
EMAIL = os.getenv('EMAIL_TO')
PROFILE = 'homework'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': [EMAIL],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_train_model():
    try:
        result = subprocess.run(
            ['python3', '/opt/airflow/dags/python_scripts/train_model.py'],
            check=True,
            capture_output=True,  # Capture stdout and stderr
            text=True  # Decode output to string (instead of bytes)
        )
        print("Output:", result.stdout)  # Print stdout (if any)
        print("Error:", result.stderr)  # Print stderr (if any)
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        raise

def dag_success_callback(context):
    logging.info("✅ Success callback triggered for DAG: %s", context['dag'].dag_id)

    subject = f"DAG {context['dag'].dag_id} succeeded ✅"
    body = f"""
    <h3>DAG Succeeded</h3>
    <p><b>DAG:</b> {context['dag'].dag_id}</p>
    <p><b>Run ID:</b> {context['run_id']}</p>
    <p><b>Execution Date:</b> {context['execution_date']}</p>
    <p><a href="{context['task_instance'].log_url}">View Logs</a></p>
    """
    try:
        send_email(to='your_email@example.com', subject=subject, html_content=body)
        logging.info("📧 Success email sent")
    except Exception as e:
        logging.error("❌ Failed to send success email: %s", str(e))


dag = DAG(
    'process_iris',
    default_args=default_args,
    description='Run dbt transformations for the iris data and use it for ML training',
    schedule_interval='0 1 * * *',
    start_date=datetime(2025, 4, 22),
    end_date=datetime(2025, 4, 25),
    catchup=True,
    tags=['dbt', 'ML_training'],
    on_success_callback=dag_success_callback
)

# Environment variables to pass to dbt
env_vars = {
    'ANALYTICS_DB': ANALYTICS_DB,
    'DBT_PROFILE': PROFILE
}

# Example of variables to pass to dbt
dbt_vars = {
    'is_test': False,
    'data_date': '{{ ds }}',  # Uses Airflow's ds (execution date) macro
}


start = DummyOperator(task_id='start', dag=dag)

# Step 1: Run dbt run to execute models
dbt_run = DbtOperator(
    task_id='dbt_run',
    dag=dag,
    command='run',
    profile=PROFILE,
    project_dir=PROJECT_DIR,
    models=['staging', 'mart'],
    env_vars=env_vars,
    vars=dbt_vars,
)

# Step 2: Run ML classification
ml_run = PythonOperator(
    task_id='ml_run',
    dag=dag,
    python_callable=run_train_model,
    # env_vars=env_vars,
)

end = DummyOperator(task_id='end', dag=dag)

#Task dependencies
start >> dbt_run >> ml_run >> end