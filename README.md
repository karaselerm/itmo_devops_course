# Лабораторная работа №2
## Тема: Airflow + Spark

## Цель
Подключить Apache Airflow к Apache Spark и запускать spark-job через DAG.

## Состав
- `Dockerfile`
- `docker-compose.yml`
- `dags/spark_sales_pipeline.py`
- `spark/sales_kpi_job.py`
- `CHANGES.md`

## Что реализовано
- Установлены зависимости для Spark в образ Airflow:
  - `procps`, `default-jre`
  - `apache-airflow-providers-apache-spark==4.1.1`
  - `pyspark==3.5.0`
- Добавлены сервисы `spark-master` и `spark-worker`.
- Реализован DAG `spark_sales_pipeline` на `SparkSubmitOperator`.
- Реализован spark-job `sales_kpi_job.py` с использованием `SparkSession`.

## Запуск
```bash
docker compose up -d --build
```

## Spark Connection в Airflow
`Admin -> Connections -> +`
- Connection Id: `spark_local`
- Connection Type: `Spark`
- Host: `spark://spark-master`
- Port: `7077`

## Проверка
```bash
docker compose ps
docker compose exec -T airflow-webserver airflow dags list | grep spark_sales_pipeline
```

Далее запустить DAG `spark_sales_pipeline` в Airflow UI.
Проверка Spark UI: `http://localhost:4040` (должны быть worker и выполненная job).
