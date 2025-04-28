

---

# 🎵 Spotify ETL with Apache Airflow

This project extracts Spotify data, transforms it using Pandas, and loads it into Snowflake using Airflow DAGs.

---

## 🚀 Technologies Used
- **Apache Airflow** — Workflow orchestration
- **Pandas** — Data cleaning and transformation
- **Snowflake** — Cloud data warehouse
- **Python** — Core programming language
- **Ubuntu WSL2** — Development environment

---

## ⚙️ How to Run

1. **Set up virtual environment**
   ```bash
   python3 -m venv airflow_venv
   source airflow_venv/bin/activate
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Airflow**
   ```bash
   export AIRFLOW_HOME=~/MSP/airflow
   airflow db init
   airflow webserver --port 8080
   airflow scheduler
   ```

4. **Trigger the DAG**
   - Access Airflow UI (`http://localhost:8080`)
   - Enable and trigger the `spotify_pipeline` DAG manually

---

## 📂 Folder Structure

```bash
MSP/
├── airflow/          # Airflow home directory
│   └── dags/         # DAG files (spotify_pipeline.py)
├── scripts/          # Python scripts for Extract, Transform, Load
├── db/               # Database related files
├── cleaned_artist_streams.csv
├── cleaned_playlists.csv
├── cleaned_playlists_tracks_streams.csv
├── Dockerfile (optional)
├── docker-compose.yml (optional)
├── requirements.txt
└── README.md
```

---

## 📌 Notes

- **Virtual environment (`airflow_venv/`)** is not uploaded to GitHub.
- Snowflake credentials should be set via `.env` file.
- Tested in **Ubuntu WSL2** environment.



