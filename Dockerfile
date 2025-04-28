FROM apache/airflow:2.10.5
USER root
RUN mkdir -p /opt/airflow/db /opt/airflow/airflow/dags /opt/airflow/scripts && \
    chown -R 50000:0 /opt/airflow/db /opt/airflow/airflow /opt/airflow/scripts
USER airflow
WORKDIR /opt/airflow
COPY --chown=airflow:0 requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=airflow:0 scripts/ scripts/
COPY --chown=airflow:0 airflow/dags/ airflow/dags/
COPY --chown=airflow:0 .env .
ENV PYTHONWARNINGS="ignore:invalid escape sequence,ignore:DISTINCT ON is currently supported only by the PostgreSQL dialect"