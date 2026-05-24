# syntax=docker/dockerfile:1.6
FROM apache/airflow:2.7.1

USER root
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends default-jre-headless procps && \
    rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow

COPY requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=/home/airflow/.cache/pip,uid=50000,gid=0 \
    pip3 install -r /tmp/requirements.txt

COPY dags/ /opt/airflow/dags/
COPY spark/ /opt/airflow/spark/
