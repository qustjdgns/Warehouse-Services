import os

from kafka import KafkaProducer, KafkaConsumer

import json



KAFKA_HOST = os.getenv(
    "KAFKA_HOST",
    "localhost:9092"
)




def create_producer():

    return KafkaProducer(

        bootstrap_servers=KAFKA_HOST,

        value_serializer=lambda data:
            json.dumps(data).encode("utf-8")

    )





def create_consumer(topic, group_id):

    return KafkaConsumer(

        topic,

        bootstrap_servers=KAFKA_HOST,

        value_deserializer=lambda data:
            json.loads(
                data.decode("utf-8")
            ),

        group_id=group_id,

        auto_offset_reset="latest"

    )
