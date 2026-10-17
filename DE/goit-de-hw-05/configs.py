import os


kafka_config = {
    "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP", "77.81.230.104:9092").split(","),
    "security_protocol": os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_PLAINTEXT"),
    "sasl_mechanism": os.getenv("KAFKA_SASL_MECHANISM", "PLAIN"),
    "username": os.getenv("KAFKA_USERNAME", "admin"),
    "password": os.getenv("KAFKA_PASSWORD", "VawEzo1ikLtrA8Ug8THa"),
}


def connection_params():
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

# дуже приємно
my_name = "oleksandr"

TOPIC_SENSORS = f"{my_name}_building_sensors"
TOPIC_TEMP_ALERTS = f"{my_name}_temperature_alerts"
TOPIC_HUMIDITY_ALERTS = f"{my_name}_humidity_alerts"

# Порогові значення
TEMP_MAX = 40      
HUMIDITY_MAX = 80  
HUMIDITY_MIN = 20
