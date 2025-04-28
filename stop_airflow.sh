#!/bin/bash

echo "🛑 Stopping Airflow processes..."

# Find and kill airflow scheduler
scheduler_pid=$(ps aux | grep "airflow scheduler" | grep -v grep | awk '{print $2}')
if [ -n "$scheduler_pid" ]; then
  kill -9 $scheduler_pid
  echo "✅ Killed Airflow Scheduler (PID: $scheduler_pid)"
else
  echo "ℹ️ No Airflow Scheduler process found."
fi

# Find and kill airflow webserver (gunicorn)
webserver_pid=$(ps aux | grep "gunicorn: master \[airflow-webserver\]" | grep -v grep | awk '{print $2}')
if [ -n "$webserver_pid" ]; then
  kill -9 $webserver_pid
  echo "✅ Killed Airflow Webserver (PID: $webserver_pid)"
else
  echo "ℹ️ No Airflow Webserver process found."
fi

# (Optional) Remove stale PID files
if [ -f ~/MSP/airflow/airflow-webserver.pid ]; then
  rm ~/MSP/airflow/airflow-webserver.pid
  echo "🧹 Removed stale PID file."
fi

echo "🛑 All Airflow services stopped!"
