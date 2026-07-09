from kafka import KafkaConsumer

import json
import os



KAFKA_HOST = os.getenv(
    "KAFKA_HOST",
    "localhost:9092"
)



consumer = KafkaConsumer(

    "low-stock",

    bootstrap_servers=KAFKA_HOST,

    value_deserializer=lambda data:
        json.loads(data.decode("utf-8")),

    group_id="notification-service",

    auto_offset_reset="latest"

)



print(
    "Notification Consumer Started"
)



for message in consumer:


    event = message.value



    if event.get("event_type") != "LOW_STOCK":

        continue



    print(
        "LOW STOCK ALERT"
    )


    print(
        f"""
상품명 : {event.get('name')}
바코드 : {event.get('barcode')}
현재재고 : {event.get('stock')}
"""
    )
