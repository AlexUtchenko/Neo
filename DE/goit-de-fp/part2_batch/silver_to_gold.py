"""
Частина 2, крок 3: silver -> gold.

  * читає silver/athlete_bio та silver/athlete_event_results;
  * join за athlete_id;
  * середні weight і height для кожної комбінації sport, medal, sex, country_noc;
  * колонка timestamp — час виконання програми;
  * запис у gold/avg_stats.
"""
import argparse
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

DEFAULT_LAKE = Path(__file__).resolve().parent / "data"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--lake-root", default=str(DEFAULT_LAKE))
    args = p.parse_args()
    lake = Path(args.lake_root)

    spark = SparkSession.builder.appName("SilverToGold").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    bio = spark.read.parquet(str(lake / "silver" / "athlete_bio"))
    results = spark.read.parquet(str(lake / "silver" / "athlete_event_results"))

    # String -> числові типи. try_cast: нечислові -> NULL, без падіння в ANSI-режимі Spark 4.
    bio = (
        bio.select(
            F.expr("try_cast(athlete_id AS BIGINT)").alias("athlete_id"),
            "sex",
            "country_noc",
            F.expr("try_cast(height AS DOUBLE)").alias("height"),
            F.expr("try_cast(weight AS DOUBLE)").alias("weight"),
        )
        .filter(F.col("height").isNotNull() & F.col("weight").isNotNull())
    )
    results = results.select(
        F.expr("try_cast(athlete_id AS BIGINT)").alias("athlete_id"),
        "sport",
        # відсутність медалі -> явна категорія
        F.coalesce(F.col("medal"), F.lit("No medal")).alias("medal"),
    )

    # join за athlete_id (country_noc — з біо: країна походження атлета)
    joined = results.join(bio, on="athlete_id", how="inner")

    gold = (
        joined.groupBy("sport", "medal", "sex", "country_noc")
        .agg(
            F.avg("weight").alias("avg_weight"),
            F.avg("height").alias("avg_height"),
        )
        .withColumn("timestamp", F.current_timestamp())
    )

    out = lake / "gold" / "avg_stats"
    gold.write.mode("overwrite").parquet(str(out))

    saved = spark.read.parquet(str(out))
    print(f"[gold/avg_stats] rows={saved.count()}")
    saved.orderBy("sport", "country_noc", "sex", "medal").show(20, truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
