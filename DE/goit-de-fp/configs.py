"""
Спільні налаштування фінального проєкту (Частина 1 — streaming).

Значення беруться зі змінних середовища, якщо вони задані,
інакше — з дефолтів нижче. ВПИШІТЬ свої credentials, які надав курс.
Не комітьте реальні паролі в публічний репозиторій.
"""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- MySQL ---
mysql_config = {
    "host": os.getenv("MYSQL_HOST", "217.61.57.46"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    # БД-джерело (athlete_bio, athlete_event_results)
    "source_db": os.getenv("MYSQL_SOURCE_DB", "olympic_dataset"),
    # БД, у яку пишемо результат (етап 6.b). Курс зазвичай дає свою схему,
    # напр. "neo_data" — уточніть у завданні/чаті курсу.
    "target_db": os.getenv("MYSQL_TARGET_DB", "neo_data"),
    "target_table": os.getenv("MYSQL_TARGET_TABLE", "oleksandr_u_athlete_enriched_agg"),
    "user": os.getenv("MYSQL_USER", "username"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "driver": "com.mysql.cj.jdbc.Driver",
}


def jdbc_url(db: str) -> str:
    return f"jdbc:mysql://{mysql_config['host']}:{mysql_config['port']}/{db}"


# MySQL JDBC-драйвер (лежить у корені проєкту)
MYSQL_JAR = str(PROJECT_ROOT / "mysql-connector-j-8.0.32.jar")

# ---------------------------------------------------------------- Kafka ---
kafka_config = {
    "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP", "77.81.230.104:9092"),
    # PLAINTEXT — для локального брокера без авторизації;
    # SASL_PLAINTEXT + PLAIN — для брокера курсу.
    "security_protocol": os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_PLAINTEXT"),
    "sasl_mechanism": os.getenv("KAFKA_SASL_MECHANISM", "PLAIN"),
    "username": os.getenv("KAFKA_USER", "admin"),
    "password": os.getenv("KAFKA_PASSWORD", "password"),
}

# Префікс, щоб ваші топіки не перетиналися з топіками інших студентів
TOPIC_PREFIX = os.getenv("TOPIC_PREFIX", "oleksandr_u")
INPUT_TOPIC = f"{TOPIC_PREFIX}_athlete_event_results"
OUTPUT_TOPIC = f"{TOPIC_PREFIX}_athlete_enriched_agg"


def kafka_options() -> dict:
    """Опції для spark.read/readStream/write .format('kafka')."""
    opts = {
        "kafka.bootstrap.servers": kafka_config["bootstrap_servers"],
        "kafka.security.protocol": kafka_config["security_protocol"],
    }
    if kafka_config["security_protocol"].startswith("SASL"):
        opts["kafka.sasl.mechanism"] = kafka_config["sasl_mechanism"]
        opts["kafka.sasl.jaas.config"] = (
            "org.apache.kafka.common.security.plain.PlainLoginModule required "
            f'username="{kafka_config["username"]}" '
            f'password="{kafka_config["password"]}";'
        )
    return opts


def spark_packages() -> str:
    """Kafka-конектор під встановлену версію Spark (Scala 2.13)."""
    import pyspark

    return f"org.apache.spark:spark-sql-kafka-0-10_2.13:{pyspark.__version__}"
