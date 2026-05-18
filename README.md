# Лабораторная работа №3
## Тема: CI/CD для Airflow + Spark

## 1. Цель работы
Добавить pipeline для проекта из ЛР2: тестирование структуры, сборку Docker-образа и деплой через Docker Compose.

## 2. Вариант реализации
Вместо GitLab CI/CD используется GitHub Actions.

## 3. Содержимое репозитория
- `.github/workflows/lab3-ci.yml` — CI/CD pipeline.
- `Dockerfile` — кастомный образ Airflow с зависимостями для Spark.
- `docker-compose.yml` — сервисы Airflow, PostgreSQL, Spark master/worker.
- `dags/spark_sales_pipeline.py` — DAG для запуска Spark-задачи.
- `spark/sales_kpi_job.py` — PySpark-скрипт.
- `CHANGES.md` — список изменений по лабораторным работам.

## 4. Pipeline
Pipeline состоит из трех jobs:
- `test`
- `build`
- `deploy`

### 4.1 Test
Job `test` запускается во всех ветках.

Проверяется:
- наличие директории `dags/`;
- наличие директории `spark/`;
- наличие `Dockerfile`;
- наличие `docker-compose.yml`;
- валидность Docker Compose конфигурации.

### 4.2 Build
Job `build` запускается после `test`.

Сборка не выполняется автоматически для веток с префиксом `feature/`.

Собирается образ:
```bash
itmo-airflow-spark:lab3
```

### 4.3 Deploy
Job `deploy` запускается после `build` автоматически только для веток:
- `main`
- `master`
- `develop`

Деплой выполняется командой:
```bash
docker compose up -d --build
```

После проверки контейнеров окружение останавливается:
```bash
docker compose down -v
```

## 5. Runner
Все jobs выполняются на runner с label:
```bash
ubuntu-latest
```

В GitHub Actions это задается через `runs-on`.

## 6. Локальная проверка
Проверить Docker Compose:
```bash
docker compose config -q
```

Собрать образ:
```bash
docker build -t itmo-airflow-spark:lab3 .
```

Запустить стек:
```bash
mkdir -p logs plugins
chmod -R 777 logs plugins
docker compose up -d --build
```

Если порт `8080` занят:
```bash
AIRFLOW_WEBSERVER_PORT=18080 docker compose up -d --build
```

Проверить контейнеры:
```bash
docker compose ps
```

Остановить стек:
```bash
docker compose down -v
```
