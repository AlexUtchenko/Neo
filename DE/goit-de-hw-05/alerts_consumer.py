"""Підписується на temperature_alerts та humidity_alerts і виводить сповіщення."""

from kafka import KafkaConsumer
from configs import connection_params, my_name, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS
import json

# Створення Kafka Consumer
consumer = KafkaConsumer(
    **connection_params(),
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    key_deserializer=lambda v: json.loads(v.decode("utf-8")) if v else None,
    auto_offset_reset="earliest",  # Зчитування повідомлень з початку
    enable_auto_commit=True,
    group_id=f"{my_name}_alerts_consumer",
)

consumer.subscribe([TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS])
print(f"Subscribed to topics '{TOPIC_TEMP_ALERTS}', '{TOPIC_HUMIDITY_ALERTS}'")

ICONS = {"temperature": "🌡️ TEMPERATURE", "humidity": "💧 HUMIDITY"}

try:
    for msg in consumer:
        a = msg.value
        print(f"{ICONS.get(a['alert_type'], 'ALERT')} ALERT | sensor {a['sensor_id']} | "
              f"{a['timestamp']} | t={a['temperature']}°C h={a['humidity']}% | {a['message']}")
except KeyboardInterrupt:
    print("\nStopped by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    consumer.close()
