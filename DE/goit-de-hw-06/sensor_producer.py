"""Імітація одного датчика yна базі попереднього ДЗ.
Один запуск = один датчик з постійним ID. Для кількох датчиків — кілька терміналів.

Режими генерації:
  walk    (за замовчуванням) — випадкове блукання в межах 25..45 °C та 15..85 %:
          значення випадкові, але змінюються плавно, як у реального датчика.
  uniform — незалежні рівномірні значення, як у в минулому ДЗ, але вони тоді майже завжди ≈35 °C / ≈50 %,
  і алерти практично не спрацьовують.
"""
from kafka import KafkaProducer
from configs import connection_params, TOPIC_SENSORS
from datetime import datetime, timezone
import argparse
import json
import random
import time

T_MIN, T_MAX = 25, 45
H_MIN, H_MAX = 15, 85

parser = argparse.ArgumentParser(description="IoT sensor simulator")
parser.add_argument("--mode", choices=["walk", "uniform"], default="walk")
parser.add_argument("--count", type=int, default=0, help="кількість повідомлень (0 = нескінченно)")
parser.add_argument("--interval", type=float, default=2.0, help="інтервал між повідомленнями, с")
args = parser.parse_args()


def bounded_walk(value, step, lo, hi):
    """Крок випадкового блукання з відбиттям від меж діапазону."""
    value += random.uniform(-step, step)
    if value < lo:
        value = 2 * lo - value
    if value > hi:
        value = 2 * hi - value
    return value


# ID датчика — випадкове, але постійне в межах одного запуску
sensor_id = random.randint(1000, 9999)
temperature = random.uniform(T_MIN, T_MAX)
humidity = random.uniform(H_MIN, H_MAX)

producer = KafkaProducer(
    **connection_params(),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print(f"Sensor {sensor_id} started ({args.mode}) -> topic '{TOPIC_SENSORS}'")

i = 0
try:
    while args.count == 0 or i < args.count:
        if args.mode == "walk":
            temperature = bounded_walk(temperature, 1.0, T_MIN, T_MAX)
            humidity = bounded_walk(humidity, 3.0, H_MIN, H_MAX)
        else:
            temperature = random.uniform(T_MIN, T_MAX)
            humidity = random.uniform(H_MIN, H_MAX)

        data = {
            "id": sensor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
        }
        try:
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
