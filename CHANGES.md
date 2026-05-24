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

## 2026-05-24
- Добавлена переменная окружения `AIRFLOW_CONN_SPARK_LOCAL=spark://spark-master:7077` в `airflow-common-env`, чтобы Airflow автоматически регистрировал Spark-коннект без ручного создания через UI.

## 2026-05-24 (ЛР4)
- В `requirements.txt` добавлен `airflow-exporter==1.7.0` — поднимает Prometheus-эндпоинт `/admin/metrics/` на webserver Airflow с метриками `airflow_dag_status`, `airflow_task_status`, `airflow_dag_last_status`, `airflow_dag_run_duration`.
- В `docker-compose.yml` добавлены сервисы `loki` (3.2.0), `alloy` (v1.5.1), `prometheus` (v2.48.1), `grafana` (11.2.0). Для Grafana проброшен порт `${GRAFANA_PORT:-3030}:3000` (стандартный 3000 был занят локально другим сервисом).
- В сервисы `spark-master` и `spark-worker` добавлено монтирование `./logs/spark-master` и `./logs/spark-worker` в `/opt/spark/logs`, чтобы Alloy мог собирать логи Spark.
- Добавлен `alloy.conf` с двумя `local.file_match` (`airflow_logs` и `spark_logs`) и пересылкой в Loki.
- Добавлен `prometheus.yml` с job-ом `airflow` и target-ом `airflow-webserver:8080/admin/metrics/`.
- Добавлен `grafana/provisioning/datasources/datasources.yml` с автоматической регистрацией Loki и Prometheus.
- Добавлен `grafana/provisioning/dashboards/dashboards.yml` + дашборд `airflow-overview.json` с двумя плитками: логи ERROR/EXCEPTION из Loki и таймсерия `airflow_dag_status{status="failed"}` из Prometheus.
