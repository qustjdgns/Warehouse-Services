from kafka import KafkaConsumer, KafkaProducer

from services.product_service import outbound_stock

import json
import os


KAFKA_HOST = os.getenv(
    "KAFKA_HOST",
    "localhost:9092"
)


consumer = KafkaConsumer(

    "stock-update",

    bootstrap_servers=KAFKA_HOST,

    value_deserializer=lambda data:
        json.loads(data.decode("utf-8")),

    group_id="stock-service",

    auto_offset_reset="latest"

)



producer = KafkaProducer(

    bootstrap_servers=KAFKA_HOST,

    value_serializer=lambda data:
        json.dumps(data).encode("utf-8")

)



print("Stock Consumer Started")



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



    if action == "OUT":


        success, result_message, product = outbound_stock(

            barcode,

            quantity,

            "kafka-consumer"

        )



        if success:


            print(
                "Stock Updated:",
                product
            )



            if product["stock"] <= 5:


                notification_event = {


                    "event_type":
                    "LOW_STOCK",


                    "barcode":
                    product["barcode"],


                    "name":
                    product["name"],


                    "stock":
                    product["stock"]

                }



                producer.send(

                    "low-stock",

                    notification_event

                )


                producer.flush()



        else:


            print(

                "Stock Update Failed:",

                result_message

            )
