# Spotify ETL Pipeline with Airflow + Snowflake + Django REST API

This project automates the extraction, transformation, and loading (ETL) of Spotify streaming data using Apache Airflow and stores the results in Snowflake. A Django REST API is provided to access and visualize the latest artist and playlist data.

---

## Features

- **ETL Workflow with Airflow**
  - Extracts artist and playlist data from Spotify using the Spotify API.
  - Cleans and transforms the data with `pandas`.
  - Loads transformed data into Snowflake tables (`artist_streams`, `playlists`, `playlist_streams`).

- **Cloud Data Warehouse**
  - Structured data is stored in **Snowflake** for scalability and analytical querying.

- **Django Dashboard**
  - Django REST API (`spotify_api`) exposes endpoints to access streaming data.
  - Built-in SQLite used for development (Django side), but Snowflake powers the core data source.

---

## Folder Structure

```
MSP/
├── airflow/                  # Airflow DAGs and final cleaned CSV files
│   ├── dags/
│   ├── logs/
│   ├── airflow.cfg
│   ├── airflow.db
│   └── cleaned_*.csv
├── dashboard/                # Django project for API dashboard
│   ├── dashboard/            # Django project settings and root URLs
│   ├── dashboard_venv/       # Virtual environment (should be gitignored)
│   └── spotify_api/          # App exposing Spotify data via REST API
├── scripts/                  # ETL scripts (called by Airflow)
│   ├── extract_spotify.py
│   ├── transform_spotify.py
│   └── load_spotify.py
├── db.sqlite3                # Local SQLite DB for Django (for development)
├── manage.py                 # Django entrypoint
├── .env                      # Environment variables for Snowflake, Spotify
├── .gitignore                # Git ignore list
├── README.md                 # You're reading it!
├── requirements.txt          # Project dependencies
├── start_airflow.sh          # Launch Airflow (scheduler + webserver)
└── stop_airflow.sh           # Shutdown Airflow
```

---

## How to Run

### 1. Environment Setup

#### (Recommended) Create virtual environments
```bash
python3 -m venv airflow_venv
source airflow_venv/bin/activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following:

#### Spotify API
```env
client_id=YOUR_SPOTIFY_CLIENT_ID
client_secret=YOUR_SPOTIFY_CLIENT_SECRET
```

#### Snowflake credentials
```env
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ROLE=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=...
SNOWFLAKE_SCHEMA=...
```

### 3. Run Airflow ETL

```bash
./start_airflow.sh
```

Access Airflow UI: [http://localhost:8081](http://localhost:8081)  
Trigger the DAG: `spotify_pipeline`

### 4. Run Django API

```bash
cd dashboard
source dashboard_venv/bin/activate
python manage.py runserver
```

API is now available at: `http://127.0.0.1:8000/api/artist-streams/`

---

## API Endpoints

| Endpoint                  | Description                       |
|---------------------------|-----------------------------------|
| `/api/artist-streams/`    | Returns latest artist stream data |
| `/api/playlists/`         | (Planned) Playlist metadata       |
| `/api/playlist-streams/`  | (Planned) Playlist track streams  |

---

## Example Use Cases

- Analyze artist popularity trends using Spotify’s top track metrics.
- Monitor playlists performance (follower count, top tracks).
- Build a data dashboard powered by Snowflake and Django REST Framework.
- Extendable for frontend dashboards (e.g., React, Chart.js).

---

## Future Work

- Add more API endpoints (e.g., by genre, popularity ranges).
- Connect to BI tools like Tableau or Superset via Snowflake.
- Add visual dashboard with Django templates or frontend framework.

---
