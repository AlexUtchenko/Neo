from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from configs import (connection_params, my_name, TOPIC_SENSORS, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS)

# Створення клієнта Kafka
admin_client = KafkaAdminClient(**connection_params())

# Визначення нових топіків
num_partitions = 2
replication_factor = 1

topic_names = [TOPIC_SENSORS, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS]

for topic_name in topic_names:
    new_topic = NewTopic(name=topic_name,
                         num_partitions=num_partitions,
                         replication_factor=replication_factor)
    try:
        admin_client.create_topics(new_topics=[new_topic], validate_only=False)
        print(f"Topic '{topic_name}' created successfully.")
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating '{topic_name}': {e}")

# Перевіряємо список існуючих топіків
print("\nMy topics:")
for topic in sorted(admin_client.list_topics()):
    if my_name in topic:
        print(f"  - {topic}")

# Закриття зв'язку з клієнтом
admin_client.close()
