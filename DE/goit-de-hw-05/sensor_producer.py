from kafka import KafkaProducer
from configs import connection_params, TOPIC_SENSORS
from datetime import datetime, timezone
import argparse
import json
import random
import time

parser = argparse.ArgumentParser(description="IoT sensor simulator")
parser.add_argument("--count", type=int, default=0, help="кількість повідомлень (0 = нескінченно)")
parser.add_argument("--interval", type=float, default=2.0, help="інтервал між повідомленнями, с")
args = parser.parse_args()

# ID датчика — випадкове, але постійне в межах одного запуску
sensor_id = random.randint(1000, 9999)

# Створення Kafka Producer
producer = KafkaProducer(
    **connection_params(),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print(f"Sensor {sensor_id} started -> topic '{TOPIC_SENSORS}'")

i = 0
try:
    while args.count == 0 or i < args.count:
        data = {
            "sensor_id": sensor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "temperature": round(random.uniform(25, 45), 2),
            "humidity": round(random.uniform(15, 85), 2),
        }
        try:
            # ключ = sensor_id: повідомлення одного датчика потрапляють в одну партицію
            producer.send(TOPIC_SENSORS, key=sensor_id, value=data)
            producer.flush()
            print(f"[{i}] sent: {data}")
        except Exception as e:
            print(f"An error occurred: {e}")
        i += 1
        time.sleep(args.interval)
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    producer.close()
