FROM apache/airflow:2.7.1

WORKDIR /opt/airflow

USER root
RUN apt update && apt -y install procps default-jre && apt clean && rm -rf /var/lib/apt/lists/*

USER airflow
COPY dags/ /opt/airflow/dags/
COPY spark/ /opt/airflow/spark/
RUN pip3 install --no-cache-dir apache-airflow-providers-apache-spark==4.1.1 pyspark==3.5.0
