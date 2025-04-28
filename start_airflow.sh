#!/bin/bash

# 1. Activate virtual environment
echo "🔵 Activating virtual environment..."
source ~/MSP/airflow_venv/bin/activate

# 2. Export AIRFLOW_HOME
echo "🔵 Setting AIRFLOW_HOME..."
export AIRFLOW_HOME=~/MSP/airflow

# 3. Remove stale PID if exists
if [ -f "$AIRFLOW_HOME/airflow-webserver.pid" ]; then
    echo "⚠️ Removing stale PID file..."
    rm "$AIRFLOW_HOME/airflow-webserver.pid"
fi

# 4. Upgrade Airflow DB
echo "🔵 Upgrading Airflow database..."
airflow db upgrade

# 5. Start scheduler
echo "🟢 Starting Airflow Scheduler..."
airflow scheduler &

# 6. Start webserver on port 8081
echo "🟢 Starting Airflow Webserver on port 8081..."
airflow webserver --port 8081 &

echo "✅ Airflow started! Access it at: http://localhost:8081"
