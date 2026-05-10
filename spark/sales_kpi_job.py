from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round as spark_round, sum as spark_sum, countDistinct


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("sales_kpi_job")
        .master("spark://spark-master:7077")
        .getOrCreate()
    )

    data = [
        (1, "books", 900.0, 2, 0.10),
        (2, "books", 1400.0, 1, 0.00),
        (3, "games", 3200.0, 1, 0.15),
        (4, "electronics", 15900.0, 1, 0.05),
        (5, "games", 2900.0, 2, 0.20),
        (6, "books", 500.0, 3, 0.00),
    ]
    columns = ["order_id", "category", "price", "qty", "discount"]

    df = spark.createDataFrame(data, columns)

    enriched = (
        df.withColumn("gross_revenue", col("price") * col("qty"))
        .withColumn("net_revenue", spark_round(col("gross_revenue") * (1 - col("discount")), 2))
    )

    category_metrics = (
        enriched.groupBy("category")
        .agg(
            spark_round(spark_sum("gross_revenue"), 2).alias("gross_revenue"),
            spark_round(spark_sum("net_revenue"), 2).alias("net_revenue"),
            spark_sum("qty").alias("items_sold"),
            countDistinct("order_id").alias("orders_count"),
        )
        .orderBy(col("net_revenue").desc())
    )

    total_metrics = enriched.agg(
        spark_round(spark_sum("gross_revenue"), 2).alias("total_gross_revenue"),
        spark_round(spark_sum("net_revenue"), 2).alias("total_net_revenue"),
        spark_sum("qty").alias("total_items_sold"),
        countDistinct("order_id").alias("total_orders"),
    )

    print("=== TOTAL METRICS ===")
    total_metrics.show(truncate=False)
    print("=== CATEGORY METRICS ===")
    category_metrics.show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
