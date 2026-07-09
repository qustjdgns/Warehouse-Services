from config.kafka import create_consumer, create_producer
from services.product_service import outbound_stock



consumer = create_consumer(
    "stock-update",
    "stock-service"
)


producer = create_producer()



print(
    "Stock Consumer Started"
)



for message in consumer:


    event = message.value



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


                producer.send(

                    "low-stock",

                    {

                        "event_type":
                        "LOW_STOCK",

                        "barcode":
                        product["barcode"],

                        "name":
                        product["name"],

                        "stock":
                        product["stock"]

                    }

                )


                producer.flush()



        else:


            print(
                "Stock Update Failed:",
                result_message
            )
