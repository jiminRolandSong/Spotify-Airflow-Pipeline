# Spotify ETL Pipeline with Apache Airflow

This project builds a full ETL (Extract, Transform, Load) pipeline using Apache Airflow to process Spotify data and load it into a Snowflake database.

---

## Technologies Used
- **Apache Airflow**: Workflow orchestration
- **Pandas**: Data cleaning and transformation
- **Snowflake**: Cloud data warehouse
- **Python**: ETL scripting
- **Ubuntu WSL2**: Development environment
- **Git & GitHub**: Version control and repository hosting

---

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/jiminRolandSong/Spotify-Airflow-Pipeline.git
cd Spotify-Airflow-Pipeline
```

2. **Create and activate a virtual environment**
```bash
python3 -m venv airflow_venv
source airflow_venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up Airflow home**
```bash
export AIRFLOW_HOME=~/MSP/airflow
```

5. **Initialize Airflow database**
```bash
airflow db migrate
```

6. **Create Airflow user** (only first time)
```bash
airflow users create \
    --username admin \
    --firstname FIRST \
    --lastname LAST \
    --role Admin \
    --email admin@example.com
```

7. **Start Airflow services**
```bash
./start_airflow.sh
```

8. **Access Airflow UI**
- Navigate to: [http://localhost:8081](http://localhost:8081)

9. **Trigger the DAG**
- Find `spotify_pipeline` in the Airflow UI and trigger it manually.

---

## Folder Structure

```
Spotify-Airflow-Pipeline/
|├── airflow/            # Airflow home directory
|├── airflow_venv/        # Python virtual environment
|├── db/                 # Database-related files (airflow.db)
|├── scripts/            # Python ETL scripts (extract, transform, load)
|├── cleaned_*.csv       # Cleaned datasets for Snowflake
|├── Dockerfile, docker-compose.yml  # (optional) For containerization
|└── README.md
```

---

## Main Flow

1. **Extract**: Pull raw data from Spotify API
2. **Transform**: Clean and reformat the data using Pandas
3. **Load**: Upload the cleaned data into Snowflake tables

---

## What's Next
- Build a Django backend to visualize ETL pipeline results
- Add real-time data updates
- Deploy Airflow and Django on AWS or GCP

---


## Quick Start Command

```bash
source airflow_venv/bin/activate
./start_airflow.sh
```🎶