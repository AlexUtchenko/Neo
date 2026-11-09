"""
Частина 1, етап 3 (продюсер): читання MySQL-таблиці athlete_event_results
і запис її рядків у Kafka-топік у форматі JSON.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyspark.sql import SparkSession 
from pyspark.sql import functions as F

from configs import (
    INPUT_TOPIC, MYSQL_JAR, jdbc_url, kafka_options, mysql_config, spark_packages,
)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0,
                   help="обмежити к-сть рядків (0 = вся таблиця)")
    args = p.parse_args()

    spark = (
        SparkSession.builder.appName("P1_MySQL_to_Kafka")
        .config("spark.jars", MYSQL_JAR)
        .config("spark.jars.packages", spark_packages())
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Читання athlete_event_results з MySQL
    results = (
        spark.read.format("jdbc")
        .options(
            url=jdbc_url(mysql_config["source_db"]),
            driver=mysql_config["driver"],
            dbtable="athlete_event_results",
            user=mysql_config["user"],
            password=mysql_config["password"],
        )
        .load()
    )
    if args.limit:
        results = results.limit(args.limit)

    print(f"athlete_event_results: rows={results.count()}")
    results.printSchema()
    results.show(5, truncate=False)

    # Серіалізація кожного рядка в JSON і запис у вхідний Kafka-топік
    to_kafka = results.select(
        F.col("athlete_id").cast("string").alias("key"),
        F.to_json(F.struct(*results.columns)).alias("value"),
    )
    (
        to_kafka.write.format("kafka")
        .options(**kafka_options())
        .option("topic", INPUT_TOPIC)
        .save()
    )
    print(f"Записано у Kafka-топік: {INPUT_TOPIC}")
    spark.stop()


if __name__ == "__main__":
    main()
