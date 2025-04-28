📀 Spotify ETL Pipeline with Apache Airflow

📋 Project Overview
This project builds an ETL (Extract, Transform, Load) pipeline for Spotify data using Apache Airflow.
The pipeline extracts data from the Spotify API, transforms it using Pandas, and loads it into a Snowflake database, all automated via an Airflow DAG.

🚀 Tech Stack
Apache Airflow : Workflow orchestration and scheduling

Spotify API : Source of music data

Pandas : Data cleaning and transformation

Snowflake : Cloud data warehouse

Python 3.12

Ubuntu WSL2 environment

📂 Project Structure
MSP/
├── airflow/               # Airflow home directory
│   ├── dags/              # DAG files (spotify_pipeline.py)
├── airflow_venv/           # (excluded from Git) Python virtual environment
├── db/                     # Database-related files
├── scripts/                # ETL scripts (extract, transform, load)
├── cleaned_artist_streams.csv
├── cleaned_playlists.csv
├── cleaned_playlists_tracks_streams.csv
├── Dockerfile (optional)
├── docker-compose.yml (optional)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
⚙️ Setup Instructions
1. Clone the Repository

git clone https://github.com/jiminRolandSong/Spotify-Airflow-Pipeline.git
cd Spotify-Airflow-Pipeline
2. Create and Activate Virtual Environment

python3 -m venv airflow_venv
source airflow_venv/bin/activate

3. Install Required Packages

pip install -r requirements.txt

4. Initialize Airflow

export AIRFLOW_HOME=~/MSP/airflow
airflow db init
5. Start Airflow Webserver

airflow webserver --port 8080
(Visit http://localhost:8080 on your browser.)

6. Start Airflow Scheduler

airflow scheduler
🛠 Key Features
Extract : Fetch artist, playlist, and track data from the Spotify API

Transform : Clean and format the data using Pandas

Load : Insert data into Snowflake tables

Automation : Schedule daily runs using Airflow DAGs

Modularization : Separate scripts for extract, transform, and load operations

🧩 DAG Flow Overview (airflow/dags/spotify_pipeline.py)

extract_task >> transform_task >> load_task
extract_task : Fetches data from Spotify

transform_task : Cleans and reshapes the data

load_task : Loads the data into Snowflake

🎯 Project Goals
Build a production-like ETL pipeline using Apache Airflow

Practice working with the Spotify API

Store and query data efficiently on Snowflake

Learn to automate real-world data workflows

📌 Important Notes
The airflow_venv/ directory should NOT be uploaded to GitHub.

You must set up your own .env file with Snowflake credentials.

This project was tested in a WSL2 Ubuntu environment.


Deploy to production using Docker and Kubernetes

