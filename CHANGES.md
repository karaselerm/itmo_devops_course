# CHANGES

## 2026-05-10 (ЛР1)
- Добавлен Dockerfile для кастомного образа Airflow (`apache/airflow:2.7.1`).
- Добавлен docker-compose.yml для сервисов `airflow-webserver`, `airflow-scheduler`, `airflow-init`, `postgres`.
- Отключены сервисы Celery-стека и Redis.
- Переключён executor на `LocalExecutor`.
- Добавлен DAG `sales_analytics_pipeline` с вычислениями и валидацией.
- Добавлен README.md и скриншоты для отчёта.
