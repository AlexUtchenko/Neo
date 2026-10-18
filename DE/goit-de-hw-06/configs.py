import os


kafka_config = {
    "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP", "77.81.230.104:9092").split(","),
    "security_protocol": os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_PLAINTEXT"),
    "sasl_mechanism": os.getenv("KAFKA_SASL_MECHANISM", "PLAIN"),
    "username": os.getenv("KAFKA_USERNAME", "admin"),
    "password": os.getenv("KAFKA_PASSWORD", "VawEzo1ikLtrA8Ug8THa"),
}


def connection_params():
    """Параметри підключення для kafka-python."""
    params = {
        "bootstrap_servers": kafka_config["bootstrap_servers"],
        "security_protocol": kafka_config["security_protocol"],
    }
    if kafka_config["security_protocol"].startswith("SASL"):
        params.update(
            sasl_mechanism=kafka_config["sasl_mechanism"],
            sasl_plain_username=kafka_config["username"],
            sasl_plain_password=kafka_config["password"],
        )
    return params


def spark_kafka_options():
    """Ті самі параметри у форматі опцій Spark Kafka source/sink."""
    opts = {
        "kafka.bootstrap.servers": ",".join(kafka_config["bootstrap_servers"]),
        "kafka.security.protocol": kafka_config["security_protocol"],
    }
    if kafka_config["security_protocol"].startswith("SASL"):
        opts["kafka.sasl.mechanism"] = kafka_config["sasl_mechanism"]
        opts["kafka.sasl.jaas.config"] = (
            "org.apache.kafka.common.security.plain.PlainLoginModule required "
            f'username="{kafka_config["username"]}" password="{kafka_config["password"]}";'
        )
    return opts


my_name = "oleksandr"

TOPIC_SENSORS = f"{my_name}_building_sensors"
TOPIC_TEMP_ALERTS = f"{my_name}_spark_temperature_alerts"
TOPIC_HUMIDITY_ALERTS = f"{my_name}_spark_humidity_alerts"
