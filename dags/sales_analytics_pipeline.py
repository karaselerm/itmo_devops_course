from __future__ import annotations

from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="sales_analytics_pipeline",
    schedule="0 9 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["lab1", "analytics"],
)
def sales_analytics_pipeline():
    @task
    def extract_data() -> list[dict]:
        return [
            {"order_id": 1, "category": "books", "price": 900, "qty": 2, "discount": 0.10},
            {"order_id": 2, "category": "books", "price": 1400, "qty": 1, "discount": 0.00},
            {"order_id": 3, "category": "games", "price": 3200, "qty": 1, "discount": 0.15},
            {"order_id": 4, "category": "electronics", "price": 15900, "qty": 1, "discount": 0.05},
            {"order_id": 5, "category": "games", "price": 2900, "qty": 2, "discount": 0.20},
            {"order_id": 6, "category": "books", "price": 500, "qty": 3, "discount": 0.00},
        ]

    @task
    def transform_data(raw_orders: list[dict]) -> list[dict]:
        transformed = []
        for row in raw_orders:
            gross = row["price"] * row["qty"]
            net = round(gross * (1 - row["discount"]), 2)
            transformed.append({**row, "gross_revenue": gross, "net_revenue": net})
        return transformed

    @task
    def calculate_metrics(orders: list[dict]) -> dict:
        total_orders = len(orders)
        total_items = sum(row["qty"] for row in orders)
        gross_revenue = sum(row["gross_revenue"] for row in orders)
        net_revenue = sum(row["net_revenue"] for row in orders)
        avg_check = round(net_revenue / total_orders, 2)
        category_revenue = {}
        for row in orders:
            category_revenue[row["category"]] = category_revenue.get(row["category"], 0) + row["net_revenue"]
        top_category = max(category_revenue, key=category_revenue.get)
        return {
            "total_orders": total_orders,
            "total_items": total_items,
            "gross_revenue": round(gross_revenue, 2),
            "net_revenue": round(net_revenue, 2),
            "avg_check": avg_check,
            "top_category": top_category,
            "category_revenue": {k: round(v, 2) for k, v in category_revenue.items()},
        }

    @task
    def validate_metrics(metrics: dict) -> str:
        if metrics["net_revenue"] <= 0:
            raise ValueError("Net revenue must be positive")
        if metrics["avg_check"] < 500:
            return "WARNING: average check is suspiciously low"
        return "OK: metrics look healthy"

    @task
    def publish_report(metrics: dict, validation_status: str) -> None:
        print("=== Sales Analytics Report ===")
        print(f"Orders count: {metrics['total_orders']}")
        print(f"Items sold: {metrics['total_items']}")
        print(f"Gross revenue: {metrics['gross_revenue']}")
        print(f"Net revenue: {metrics['net_revenue']}")
        print(f"Average check: {metrics['avg_check']}")
        print(f"Top category: {metrics['top_category']}")
        print(f"Category revenue: {metrics['category_revenue']}")
        print(f"Validation: {validation_status}")

    raw = extract_data()
    transformed = transform_data(raw)
    metrics = calculate_metrics(transformed)
    status = validate_metrics(metrics)
    publish_report(metrics, status)


sales_analytics_pipeline()
