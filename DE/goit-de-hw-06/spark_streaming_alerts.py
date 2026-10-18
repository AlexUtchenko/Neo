import os
import pyspark
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from configs import (spark_kafka_options, my_name,
                     TOPIC_SENSORS, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONDITIONS_PATH = os.path.join(BASE_DIR, "alerts_conditions.csv")
CHECKPOINT_DIR = os.path.join(BASE_DIR, "checkpoints")

# Пакет-конектор Kafka під версію встановленого Spark
KAFKA_PACKAGE = f"org.apache.spark:spark-sql-kafka-0-10_2.13:{pyspark.__version__}"

WINDOW_DURATION = "1 minute"
SLIDING_INTERVAL = "30 seconds"
WATERMARK = "10 seconds"

# Схема JSON із топіку. sensor_id — для сумісності зі старими повідомленнями з ДЗ_5.
sensor_schema = StructType([
    StructField("id", IntegerType()),
    StructField("sensor_id", IntegerType()),
    StructField("timestamp", StringType()),
    StructField("temperature", DoubleType()),
    StructField("humidity", DoubleType()),
])


def parse_sensors(raw: DataFrame) -> DataFrame:
    """value (bytes з Kafka) -> id, timestamp, temperature, humidity."""
    return (raw
            .select(F.from_json(F.col("value").cast("string"), sensor_schema).alias("d"))
            .select(F.coalesce("d.id", "d.sensor_id").alias("id"),
                    F.to_timestamp("d.timestamp").alias("timestamp"),
                    F.col("d.temperature").alias("temperature"),
                    F.col("d.humidity").alias("humidity"))
            .where(F.col("timestamp").isNotNull()))


def aggregate(sensors: DataFrame) -> DataFrame:
    """Sliding window 1 хв / крок 30 с, watermark 10 с: середні t та h."""
    return (sensors
            .withWatermark("timestamp", WATERMARK)
            .groupBy(F.window("timestamp", WINDOW_DURATION, SLIDING_INTERVAL))
            .agg(F.avg("temperature").alias("t_avg"),
                 F.avg("humidity").alias("h_avg"),
                 F.count("*").alias("n")))


def in_range(value_col: str, min_col: str, max_col: str):
    """обробка -999, котре означає 'не використовується'."""
    v, lo, hi = F.col(value_col), F.col(min_col), F.col(max_col)
    return ((lo == -999) | (v >= lo)) & ((hi == -999) | (v <= hi))


def build_alerts(averages: DataFrame, conditions: DataFrame) -> DataFrame:
    """Cross join середніх з умовами + фільтрація."""
    return (averages.crossJoin(F.broadcast(conditions))
            .where(in_range("h_avg", "humidity_min", "humidity_max")
                   & in_range("t_avg", "temperature_min", "temperature_max"))
            .select(
                "window",
                F.round("t_avg", 2).alias("t_avg"),
                F.round("h_avg", 2).alias("h_avg"),
                F.col("code").cast("string").alias("code"),
                "message",
                F.date_format(F.current_timestamp(), "yyyy-MM-dd HH:mm:ss.SSS").alias("timestamp"),
                # алерт за вологістю -> humidity-топік, за температурою -> temperature-топік
                F.when(F.col("humidity_min") != -999, F.lit(TOPIC_HUMIDITY_ALERTS))
                 .otherwise(F.lit(TOPIC_TEMP_ALERTS)).alias("topic"),
            ))


def to_kafka(alerts: DataFrame) -> DataFrame:
    """key = code, value = JSON алерту, topic = колонка маршрутизації."""
    return alerts.select(
        "topic",
        F.col("code").alias("key"),
        F.to_json(F.struct("window", "t_avg", "h_avg", "code", "message", "timestamp")).alias("value"),
    )


def main():
    spark = (SparkSession.builder
             .appName(f"{my_name}_iot_alerts")
             .master("local[*]")
             .config("spark.jars.packages", KAFKA_PACKAGE)
             .config("spark.sql.session.timeZone", "Europe/Kyiv")
             .config("spark.sql.shuffle.partitions", "4")
             .getOrCreate())
    spark.sparkContext.setLogLevel("WARN")

    # 3. Параметри алертів із CSV (без редеплою коду)
    conditions = spark.read.csv(CONDITIONS_PATH, header=True, inferSchema=True)
    print("Alert conditions:")
    conditions.show(truncate=False)

    # 1. Потік з Kafka
    raw = (spark.readStream.format("kafka")
           .options(**spark_kafka_options())
           .option("subscribe", TOPIC_SENSORS)
           .option("startingOffsets", "latest")
           .option("failOnDataLoss", "false")
           .load())

    # 2. Агрегація
    averages = aggregate(parse_sensors(raw))
    # 4. Визначення алертів
    alerts = build_alerts(averages, conditions)

    # Консоль: середні по вікнах (update — видно, як оновлюються вікна)
    q_avg = (averages.writeStream
             .outputMode("update")
             .format("console").option("truncate", False)
             .option("checkpointLocation", os.path.join(CHECKPOINT_DIR, "averages"))
             .trigger(processingTime="10 seconds")
             .queryName("averages").start())

    # 5. Алерти -> Kafka. append: вікно публікується один раз, після закриття watermark-ом
    q_kafka = (to_kafka(alerts).writeStream
               .outputMode("append")
               .format("kafka")
               .options(**spark_kafka_options())
               .option("checkpointLocation", os.path.join(CHECKPOINT_DIR, "alerts_kafka"))
               .trigger(processingTime="10 seconds")
               .queryName("alerts_to_kafka").start())

    # Консоль: ті самі алерти, що йдуть у Kafka
    q_alerts = (alerts.writeStream
                .outputMode("append")
                .format("console").option("truncate", False)
                .option("checkpointLocation", os.path.join(CHECKPOINT_DIR, "alerts_console"))
                .trigger(processingTime="10 seconds")
                .queryName("alerts_console").start())

    print(f"Reading '{TOPIC_SENSORS}' -> writing alerts to "
          f"'{TOPIC_TEMP_ALERTS}', '{TOPIC_HUMIDITY_ALERTS}'")
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
