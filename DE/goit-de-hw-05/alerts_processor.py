"""Читає дані з building_sensors, перевіряє пороги і пише сповіщення в temperature_alerts / humidity_alerts."""

from kafka import KafkaConsumer, KafkaProducer
from configs import (connection_params, my_name,
                     TOPIC_SENSORS, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS,
                     TEMP_MAX, HUMIDITY_MAX, HUMIDITY_MIN)
from datetime import datetime, timezone
import json

# Створення Kafka Consumer
consumer = KafkaConsumer(
    **connection_params(),
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    key_deserializer=lambda v: json.loads(v.decode("utf-8")) if v else None,
    auto_offset_reset="latest",   # обробляємо нові показники
    enable_auto_commit=True,
    group_id=f"{my_name}_alerts_processor",
)

# Створення Kafka Producer для сповіщень
producer = KafkaProducer(
    **connection_params(),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

consumer.subscribe([TOPIC_SENSORS])
print(f"Subscribed to topic '{TOPIC_SENSORS}'")


def make_alert(data, alert_type, threshold, message):
    return {
        "sensor_id": data["sensor_id"],
        "timestamp": data["timestamp"],                     # час вимірювання
        "alert_time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "alert_type": alert_type,
        "threshold": threshold,
        "message": message,
    }


try:
    for msg in consumer:
        data = msg.value
        t, h, sid = data["temperature"], data["humidity"], data["sensor_id"]
        print(f"Received: sensor={sid} t={t}°C h={h}% (partition {msg.partition})")

        # Перевірка температури
        if t > TEMP_MAX:
            alert = make_alert(data, "temperature", TEMP_MAX,
                               f"Temperature {t}°C exceeds threshold {TEMP_MAX}°C")
            producer.send(TOPIC_TEMP_ALERTS, key=sid, value=alert)
            print(f"  -> TEMP ALERT sent to '{TOPIC_TEMP_ALERTS}'")

        # Перевірка вологості
        if h > HUMIDITY_MAX or h < HUMIDITY_MIN:
            bound = HUMIDITY_MAX if h > HUMIDITY_MAX else HUMIDITY_MIN
            side = "above maximum" if h > HUMIDITY_MAX else "below minimum"
            alert = make_alert(data, "humidity", bound,
                               f"Humidity {h}% is {side} {bound}% "
                               f"(allowed {HUMIDITY_MIN}-{HUMIDITY_MAX}%)")
            producer.send(TOPIC_HUMIDITY_ALERTS, key=sid, value=alert)
            print(f"  -> HUMIDITY ALERT sent to '{TOPIC_HUMIDITY_ALERTS}'")

        producer.flush()
except KeyboardInterrupt:
    print("\nStopped by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    consumer.close()
    producer.close()
