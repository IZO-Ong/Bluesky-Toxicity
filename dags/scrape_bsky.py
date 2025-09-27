from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
import os

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    "scrape_bsky",
    default_args=default_args,
    description="Scrape Bluesky posts hourly",
    schedule_interval="0 * * * *",  # every hour
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
        environment={
            "DATABASE_URL": "postgresql://postgres:postgres@db:5432/bluesky",
            "BLUESKY_IDENTIFIER": os.getenv("BLUESKY_IDENTIFIER"),
            "BLUESKY_APP_PASSWORD": os.getenv("BLUESKY_APP_PASSWORD"),
        },
    )
