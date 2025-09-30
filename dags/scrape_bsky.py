from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
import os

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
}

with DAG(
    "scrape_bsky",
    default_args=default_args,
    description="Scrape Bluesky posts every 6 hours",
    schedule_interval="0 */6 * * *",   # every 6 hours
    start_date=datetime(2025, 9, 16),
    catchup=False,
) as dag:

    scrape_task = DockerOperator(
        task_id="run_scraper",
        image="bluesky-scraper:latest",
        command="python runner.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bluesky-toxicity_default",
        auto_remove=True,
        mount_tmp_dir=False,
        environment={
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "BLUESKY_IDENTIFIER": os.getenv("BLUESKY_IDENTIFIER"),
            "BLUESKY_APP_PASSWORD": os.getenv("BLUESKY_APP_PASSWORD"),
        },
    )
