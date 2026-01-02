from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta
import os

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "scrape_bsky",
    default_args=default_args,
    description="Scrape Bluesky posts and analyze toxicity every 6 hours",
    schedule_interval="0 */6 * * *",   # Runs at 00:00, 06:00, 12:00, 18:00
    start_date=datetime(2025, 9, 16),
    catchup=False,
    tags=["bluesky", "scraper", "ml"],
) as dag:

    scrape_task = DockerOperator(
        task_id="run_scraper",
        image="bluesky-scraper:latest",
        command="python runner.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bluesky-toxicity_default",
        auto_remove=True,
        mount_tmp_dir=False,
        
        mounts=[
            Mount(
                source="/home/ubuntu/.cache/torch",
                target="/root/.cache/torch",
                type="bind"
            )
        ],
        
        environment={
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "BLUESKY_IDENTIFIER": os.getenv("BLUESKY_IDENTIFIER"),
            "BLUESKY_APP_PASSWORD": os.getenv("BLUESKY_APP_PASSWORD"),
        },
    )

    scrape_task
