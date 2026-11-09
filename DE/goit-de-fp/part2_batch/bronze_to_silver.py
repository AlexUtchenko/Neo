"""
Частина 2, крок 2: bronze -> silver.

  * читає bronze/<table>;
  * застосовує clean_text (UDF) до ВСІХ текстових колонок;
  * дедублікує рядки;
  * записує silver/<table>.
"""
import argparse
import re
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

TABLES = ["athlete_bio", "athlete_event_results"]
DEFAULT_LAKE = Path(__file__).resolve().parent / "data"


def clean_text(text):
    # Функція з порад до виконанння проєкту. Доповнення: NULL лишається NULL  інакше str(None) перетворить відсутнє значення на рядок "None".
    if text is None:
        return None
    return re.sub(r'[^a-zA-Z0-9,.\"\']', '', str(text))


clean_text_udf = udf(clean_text, StringType())


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--lake-root", default=str(DEFAULT_LAKE))
    p.add_argument("--tables", nargs="+", default=TABLES)
    args = p.parse_args()
    lake = Path(args.lake_root)

    spark = SparkSession.builder.appName("BronzeToSilver").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    for table in args.tables:
        df = spark.read.parquet(str(lake / "bronze" / table))
        rows_in = df.count()

        # чистка тексту для всіх колонок типу String
        text_cols = [f.name for f in df.schema.fields
                     if isinstance(f.dataType, StringType)]
        for col_name in text_cols:
            df = df.withColumn(col_name, clean_text_udf(df[col_name]))

        # дедублікація рядків (після чистки — щоб "a b" і "ab" злилися)
        df = df.dropDuplicates()

        out = lake / "silver" / table
        df.write.mode("overwrite").parquet(str(out))
        rows_out = spark.read.parquet(str(out)).count()
        print(f"[silver/{table}] rows: bronze={rows_in} -> silver={rows_out} "
              f"(видалено дублікатів: {rows_in - rows_out}); "
              f"очищено колонок: {len(text_cols)}")
        spark.read.parquet(str(out)).show(10, truncate=40)

    spark.stop()


if __name__ == "__main__":
    main()
