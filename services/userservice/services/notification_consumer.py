from config.kafka import create_consumer

from services.notification_service import save_low_stock_notification




consumer = create_consumer(

    "low-stock",

    "notification-service"

)



print(
    "Notification Consumer Started"
)



for message in consumer:


    event = message.value



    if event.get(
        "event_type"
    ) != "LOW_STOCK":

        continue



    save_low_stock_notification(
        event
    )



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
