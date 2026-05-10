from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="spark_sales_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["lab2", "spark"],
) as dag:
    run_spark_sales_job = SparkSubmitOperator(
        task_id="run_spark_sales_job",
        application="/opt/airflow/spark/sales_kpi_job.py",
        name="run_spark_sales_job",
        conn_id="spark_local",
        verbose=True,
    )

    run_spark_sales_job
