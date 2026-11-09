"""
Частина 1. Building an End-to-End Streaming Pipeline.

Етапи:
  1. читання athlete_bio з MySQL;
  2. фільтрація height і weight;
  3. читання результатів змагань із Kafka-топіку + JSON -> колонки
     (запис MySQL -> Kafka робить p1_01_mysql_to_kafka.py);
  4. join з біо-даними за athlete_id;
  5. середні зріст/вага по sport, medal, sex, country_noc + timestamp;
  6. forEachBatch: a) вихідний Kafka-топік, b) MySQL.
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from configs import (  # noqa: E402
    INPUT_TOPIC, MYSQL_JAR, OUTPUT_TOPIC, PROJECT_ROOT,
    jdbc_url, kafka_options, mysql_config, spark_packages,
)

CHECKPOINT = str(PROJECT_ROOT / "checkpoints" / "part1_streaming")


def read_mysql(spark: SparkSession, table: str) -> DataFrame:
    return (
        spark.read.format("jdbc")
        .options(
            url=jdbc_url(mysql_config["source_db"]),
            driver=mysql_config["driver"],
            dbtable=table,
            user=mysql_config["user"],
            password=mysql_config["password"],
        )
        .load()
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--timeout", type=int, default=0,
                   help="зупинити стрим через N секунд (0 = працювати до Ctrl+C)")
    p.add_argument("--max-offsets", type=int, default=5000,
                   help="maxOffsetsPerTrigger — розмір мікробатчу")
    args = p.parse_args()

    spark = (
        SparkSession.builder.appName("P1_Streaming_Pipeline")
        .config("spark.jars", MYSQL_JAR)
        .config("spark.jars.packages", spark_packages())
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Зчитування фізичних показників атлетів з MySQL athlete_bio

    bio_raw = read_mysql(spark, "athlete_bio")


    # Фільтрація рядків, де height / weight порожні або не числа.
    # try_cast повертає NULL замість помилки (у Spark 4 ANSI-режим увімкнено за замовчуванням, і звичайний cast("double") на рядку "abc" кидає виняток).

    bio = (
        bio_raw
        .withColumn("height", F.expr("try_cast(height AS DOUBLE)"))
        .withColumn("weight", F.expr("try_cast(weight AS DOUBLE)"))
        .filter(F.col("height").isNotNull() & F.col("weight").isNotNull())
        .select("athlete_id", "sex", "country_noc", "height", "weight")
        .cache()  # статична сторона join — щоб не читати MySQL у кожному батчі
    )
    print(f"[Етап 2] athlete_bio: всього={bio_raw.count()}, "
          f"з валідними height/weight={bio.count()}")

    # Читання результатів змагань з Kafka-топіку.
    # Схему JSON беремо з MySQL-таблиці-джерела (load() тягне лише метадані), тож кожне поле JSON стає окремою колонкою з правильним типом.
    results_schema = read_mysql(spark, "athlete_event_results").schema

    events = (
        spark.readStream.format("kafka")
        .options(**kafka_options())
        .option("subscribe", INPUT_TOPIC)
        .option("startingOffsets", "earliest")
        .option("maxOffsetsPerTrigger", args.max_offsets)
        .option("failOnDataLoss", "false")
        .load()
        # JSON -> DataFrame (кожне поле — окрема колонка)
        .select(F.from_json(F.col("value").cast("string"), results_schema).alias("j"))
        .select("j.*")
        # відсутність медалі
        .withColumn(
            "medal",
            F.when(
                F.col("medal").isNull() | F.lower(F.trim("medal")).isin("", "nan", "na"),
                F.lit("No medal"),
            ).otherwise(F.col("medal")),
        )
        # country_noc залишаємо з біо (країна походження атлета)
        .drop("country_noc")
    )

    # Етап 4: об'єднання стриму результатів зі статичними біо-даними за ключем athlete_id (stream-static inner join)
    enriched = events.join(bio, on="athlete_id", how="inner")

    # Етап 5: середній зріст і вага для кожної комбінації sport, medal, sex, country_noc + timestamp розрахунку
    aggregated = (
        enriched.groupBy("sport", "medal", "sex", "country_noc")
        .agg(
            F.round(F.avg("height"), 3).alias("avg_height"),
            F.round(F.avg("weight"), 3).alias("avg_weight"),
        )
        .withColumn("timestamp", F.current_timestamp())
    )

    # Стрим даних через forEachBatch у два sink-и
    def foreach_batch_function(batch_df: DataFrame, batch_id: int) -> None:
        if batch_df.isEmpty():
            return
        batch_df = batch_df.persist()
        print(f"\n=== batch_id={batch_id}, rows={batch_df.count()} ===")
        batch_df.orderBy("sport", "country_noc").show(20, truncate=False)

        # Запис у вихідний Kafka-топік
        (
            batch_df.select(
                F.concat_ws("|", "sport", "medal", "sex", "country_noc").alias("key"),
                F.to_json(F.struct(*batch_df.columns)).alias("value"),
            )
            .write.format("kafka")
            .options(**kafka_options())
            .option("topic", OUTPUT_TOPIC)
            .save()
        )

        # Запис у базу даних MySQL
        (
            batch_df.write.format("jdbc")
            .option("url", jdbc_url(mysql_config["target_db"]))
            .option("driver", mysql_config["driver"])
            .option("dbtable", mysql_config["target_table"])
            .option("user", mysql_config["user"])
            .option("password", mysql_config["password"])
            .mode("append")
            .save()
        )
        batch_df.unpersist()

    query = (
        aggregated.writeStream
        .foreachBatch(foreach_batch_function)
        .outputMode("update")  # у батч потрапляють лише змінені групи
        .option("checkpointLocation", CHECKPOINT)
        .trigger(processingTime="10 seconds")
        .start()
    )
    if args.timeout:
        query.awaitTermination(args.timeout)
        # М'яка зупинка, щоб stop() не скасував задачі посеред запису
        while query.isActive and query.status["isTriggerActive"]:
            time.sleep(1)
        query.stop()
    else:
        query.awaitTermination()
    spark.stop()


if __name__ == "__main__":
    main()
