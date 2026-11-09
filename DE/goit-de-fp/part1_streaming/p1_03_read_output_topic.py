"""
Частина 1: перевірка результату — друк даних з вихідного Kafka-топіку.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType, StringType, StructField, StructType, TimestampType,
)

from configs import OUTPUT_TOPIC, kafka_options, spark_packages

OUT_SCHEMA = StructType([
    StructField("sport", StringType()),
    StructField("medal", StringType()),
    StructField("sex", StringType()),
    StructField("country_noc", StringType()),
    StructField("avg_height", DoubleType()),
    StructField("avg_weight", DoubleType()),
    StructField("timestamp", TimestampType()),
])


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=30)
    args = p.parse_args()

    spark = (
        SparkSession.builder.appName("P1_Read_Output_Topic")
        .config("spark.jars.packages", spark_packages())
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    df = (
        spark.read.format("kafka")
        .options(**kafka_options())
        .option("subscribe", OUTPUT_TOPIC)
        .option("startingOffsets", "earliest")
        .load()
        .select(
            F.col("offset"),
            F.from_json(F.col("value").cast("string"), OUT_SCHEMA).alias("v"),
        )
        .select("offset", "v.*")
    )
    print(f"Топік {OUTPUT_TOPIC}: повідомлень={df.count()}")
    df.orderBy(F.col("offset").desc()).show(args.n, truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
