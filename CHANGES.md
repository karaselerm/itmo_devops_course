# CHANGES

## 2026-05-10 (ЛР1)
- Добавлен Dockerfile для кастомного образа Airflow (`apache/airflow:2.7.1`).
- Добавлен docker-compose.yml для сервисов `airflow-webserver`, `airflow-scheduler`, `airflow-init`, `postgres`.
- Отключены сервисы Celery-стека и Redis.
- Переключён executor на `LocalExecutor`.
- Добавлен DAG `sales_analytics_pipeline` с вычислениями и валидацией.
- Добавлен README.md и скриншоты для отчёта.

## 2026-05-10 (ЛР2)
- Обновлён Dockerfile: установка `procps`, `default-jre`, `apache-airflow-providers-apache-spark==4.1.1`, `pyspark==3.5.0`.
- Добавлено копирование директории `spark` в образ.
- В docker-compose добавлены `spark-master` и `spark-worker`.
- В Airflow-сервисы добавлено монтирование `./spark:/opt/airflow/spark`.
- Добавлен DAG `spark_sales_pipeline` на `SparkSubmitOperator`.
- Добавлен spark-job `spark/sales_kpi_job.py` на `SparkSession`.
