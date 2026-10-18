"""Читає алерти, які Spark записав у вихідні топіки, і виводить на екран."""

from kafka import KafkaConsumer
from configs import connection_params, my_name, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS
import json

consumer = KafkaConsumer(
    **connection_params(),
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    key_deserializer=lambda v: v.decode("utf-8") if v else None,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=f"{my_name}_spark_alerts_reader",
)

consumer.subscribe([TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS])
print(f"Subscribed to topics '{TOPIC_TEMP_ALERTS}', '{TOPIC_HUMIDITY_ALERTS}'")

try:
    for msg in consumer:
        a = msg.value
        w = a["window"]
        print(f"[{msg.topic}] code={a['code']} {a['message']:<14} | "
              f"window {w['start'][11:19]}-{w['end'][11:19]} | "
              f"t_avg={a['t_avg']} h_avg={a['h_avg']} | {a['timestamp']}")
        print(f"    raw: {json.dumps(a)}")
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    consumer.close()
