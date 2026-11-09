"""
Частина 1: перевірка, що лежить у MySQL-таблиці результатів (для скриншоту бази даних без окремого SQL-клієнта).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from configs import MYSQL_JAR, jdbc_url, mysql_config


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=30)
    args = p.parse_args()

    spark = (
        SparkSession.builder.appName("P1_Read_MySQL_Result")
        .config("spark.jars", MYSQL_JAR)
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    table = f"{mysql_config['target_db']}.{mysql_config['target_table']}"
    df = (
        spark.read.format("jdbc")
        .options(
            url=jdbc_url(mysql_config["target_db"]),
            driver=mysql_config["driver"],
            dbtable=mysql_config["target_table"],
            user=mysql_config["user"],
            password=mysql_config["password"],
        )
        .load()
    )

    print(f"\nSELECT * FROM {table} ORDER BY timestamp DESC LIMIT {args.n};")
    print(f"Всього рядків у таблиці: {df.count()}")
    df.printSchema()
    df.orderBy(F.col("timestamp").desc()).show(args.n, truncate=False)

    print("Кількість записів за кожен мікробатч (timestamp):")
    df.groupBy("timestamp").count().orderBy("timestamp").show(50, truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
