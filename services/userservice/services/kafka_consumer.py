from kafka import KafkaConsumer

from services.product_service import outbound_stock

import json
import os



consumer = KafkaConsumer(

    "stock-update",

    bootstrap_servers=os.getenv(
        "KAFKA_HOST",
        "localhost:9092"
    ),


    value_deserializer=lambda data:
        json.loads(
            data.decode("utf-8")
        ),


    group_id="stock-service",


    auto_offset_reset="latest"

)



print(
    "Kafka Stock Consumer Started"
)



for message in consumer:


    event = message.value


    print(
        "Received Event:",
        event
    )



    if event.get("event_type") != "STOCK_UPDATE":

        continue




    barcode = event.get(
        "barcode"
    )


    quantity = event.get(
        "quantity",
        1
    )


    action = event.get(
        "action"
    )




    # 출고 이벤트

    if action == "OUT":


        success, message, product = outbound_stock(

            barcode,

            quantity,

            "kafka-consumer"

        )


        if success:

            print(
                "Stock Updated:",
                product
            )


        else:

            print(
                "Stock Update Failed:",
                message
            )
