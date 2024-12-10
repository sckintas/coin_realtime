import os
import pandas as pd
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import storage
from io import BytesIO
import requests

# Retrieve environment variables
project_id = os.environ.get("gcp_project_id")  # Set in Composer environment variables
bucket_name = os.environ.get("gcs_bucket_name")  # Set in Composer environment variables
api_key = os.environ.get("api_key")  # Set in Composer environment variables

# Construct dataset URL with the API key
dataset_url = f"https://api.coincap.io/v2/assets/bitcoin/history?interval=m1&apikey={api_key}"
parquet_filename = "bitcoin_history_{{ data_interval_end.strftime('%Y%m%d_%H%M') }}.parquet"


def fetch_and_upload_to_gcs(dataset_url, bucket_name, parquet_filename):
    """
    Fetch data from API and write it as a Parquet file directly to GCS.
    """
    # Fetch data from API
    response = requests.get(dataset_url)
    response.raise_for_status()
    json_data = response.json()

    # Convert JSON data to Pandas DataFrame
    df = pd.DataFrame.from_dict(json_data['data'])

    # Create a GCS client
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    # Convert DataFrame to Parquet in memory
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)

    # Upload Parquet file to GCS
    blob = bucket.blob(f"raw/bitcoin_history/{parquet_filename}")
    blob.upload_from_file(parquet_buffer, content_type="application/octet-stream")


# Default DAG arguments
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 12, 10),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# DAG definition
with DAG(
    dag_id="bitcoin_history_direct_to_gcs",
    schedule_interval=timedelta(minutes=5),
    default_args=default_args,
    max_active_runs=1,
    catchup=False,
    tags=['crypto-analytics'],
) as dag:

    # Task to fetch data from API and write directly to GCS
    fetch_and_upload_task = PythonOperator(
        task_id="fetch_and_upload_to_gcs",
        python_callable=fetch_and_upload_to_gcs,
        op_kwargs={
            "dataset_url": dataset_url,
            "bucket_name": bucket_name,
            "parquet_filename": parquet_filename,
        },
    )
