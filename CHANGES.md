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

## 2026-05-18 (ЛР3)
- Добавлен GitHub Actions pipeline `.github/workflows/lab3-ci.yml`.
- Добавлен stage `test` с проверкой директорий `dags/` и `spark/`, основных файлов проекта и Docker Compose конфигурации.
- Добавлен stage `build` со сборкой образа `itmo-airflow-spark:lab3`.
- Добавлен stage `deploy` с запуском проекта через `docker compose up -d --build`.
- В deploy добавлена подготовка директорий `logs/` и `plugins/` для Airflow.
- Для `deploy` добавлено ограничение на ветки `main`, `master`, `develop`.
- Для `build` добавлено отключение автоматического запуска на ветках `feature/*`.
- В `docker-compose.yml` добавлено имя образа Airflow `itmo-airflow-spark:lab3`.
