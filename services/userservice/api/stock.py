from kafka import KafkaConsumer
import json

from services.product_service import inbound_stock, outbound_stock


consumer = KafkaConsumer(
    "scan-event",
    bootstrap_servers=["kafka-service:9092"],
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)



for message in consumer:

    event = message.value


    barcode = event.get("barcode")


    print(
        "스캔 이벤트 수신:",
        barcode
    )


    # 예시: 스캔 발생 시 재고 차감
    success, message, product = outbound_stock(
        barcode,
        1
    )


    if success:
        print(
            "재고 변경 완료",
            product
        )

    else:
        print(
            "재고 변경 실패",
            message
        )
