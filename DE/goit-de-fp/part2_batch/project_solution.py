"""
Частина 2, крок 4: Airflow DAG, що послідовно запускає три Spark jobs:
landing_to_bronze -> bronze_to_silver -> silver_to_gold.
"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

try:  # Airflow 3.x
    from airflow.sdk import DAG
except ImportError:  # Airflow 2.x
    from airflow import DAG

JOBS_DIR = Path(__file__).resolve().parent
LAKE_ROOT = os.getenv("LAKE_ROOT", str(JOBS_DIR / "data"))

COMMON = dict(
    conn_id="spark-default",
    verbose=True,
    application_args=["--lake-root", LAKE_ROOT],
    conf={"spark.pyspark.python": os.getenv("PYSPARK_PYTHON", sys.executable)},
)

with DAG(
    dag_id="oleksandr_u_datalake_project",
    description="Landing -> Bronze -> Silver -> Gold (final project, part 2)",
    schedule=None,
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["final-project", "spark", "datalake"],
) as dag:
    landing_to_bronze = SparkSubmitOperator(
        task_id="landing_to_bronze",
        application=str(JOBS_DIR / "landing_to_bronze.py"),
        **COMMON,
    )

    bronze_to_silver = SparkSubmitOperator(
        task_id="bronze_to_silver",
        application=str(JOBS_DIR / "bronze_to_silver.py"),
        **COMMON,
    )

    silver_to_gold = SparkSubmitOperator(
        task_id="silver_to_gold",
        application=str(JOBS_DIR / "silver_to_gold.py"),
        **COMMON,
    )

    landing_to_bronze >> bronze_to_silver >> silver_to_gold
