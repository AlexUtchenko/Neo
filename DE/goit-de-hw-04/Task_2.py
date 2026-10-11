import os
from pyspark.sql import SparkSession

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuek-vuh3.csv")

# Створюємо сесію Spark
spark = (
    SparkSession.builder
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "2")
    .appName("MyGoitSparkSandbox")
    .getOrCreate()
)

# Завантажуємо датасет
nuek_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(CSV_PATH)
)

nuek_repart = nuek_df.repartition(2)

nuek_processed = (
    nuek_repart
    .where("final_priority < 3")
    .select("unit_id", "final_priority")
    .groupBy("unit_id")
    .count()
)

# Проміжний action: collect
nuek_processed.collect()

# Ось ТУТ додано рядок
nuek_processed = nuek_processed.where("count>2")

nuek_processed.collect()

input("Press Enter to continue...5")

# Закриваємо сесію Spark
spark.stop()