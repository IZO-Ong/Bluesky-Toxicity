from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

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
    image="bluesky-toxicity-scraper:latest",
    command="python runner.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    auto_remove=True,
    mount_tmp_dir=False,
)
