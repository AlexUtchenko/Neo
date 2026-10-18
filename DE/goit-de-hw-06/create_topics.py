from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from configs import (connection_params, my_name, TOPIC_SENSORS, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS)

# Створення клієнта Kafka
admin_client = KafkaAdminClient(**connection_params())

num_partitions = 2
replication_factor = 1

for topic_name in [TOPIC_SENSORS, TOPIC_TEMP_ALERTS, TOPIC_HUMIDITY_ALERTS]:
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

print("\nMy topics:")
for topic in sorted(admin_client.list_topics()):
    if topic.startswith(f"{my_name}_"):
        print(f"  - {topic}")

admin_client.close()
