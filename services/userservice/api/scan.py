from flask import Blueprint, request, jsonify

from services.scan_service import validate_barcode
from services.product_service import get_product

from kafka import KafkaProducer

import json
import os



scan_bp = Blueprint(
    "scan",
    __name__
)



# Kafka Producer 설정

producer = KafkaProducer(

    bootstrap_servers=os.getenv(
        "KAFKA_HOST",
        "localhost:9092"
    ),

    value_serializer=lambda data:
        json.dumps(data).encode("utf-8")

)





# -----------------------------
# QR Scan API
# -----------------------------
@scan_bp.route(
    "/scan",
    methods=["POST"]
)
def scan():


    data = request.get_json()



    if data is None:

        return jsonify({

            "error":
            "JSON body가 필요합니다."

        }),400





    barcode = data.get(
        "barcode"
    )



    # 바코드 검증

    is_valid, message = validate_barcode(
        barcode
    )



    if not is_valid:

        return jsonify({

            "error":message

        }),400





    # 상품 조회

    product = get_product(
        barcode
    )



    if product is None:

        return jsonify({

            "error":
            "상품을 찾을 수 없습니다."

        }),404





    # Kafka 이벤트 생성

    event = {


        "event_type":
        "STOCK_UPDATE",


        "barcode":
        barcode,


        "quantity":
        1,


        "action":
        "OUT"


    }





    # Kafka Topic 전송

    producer.send(

        "stock-update",

        event

    )



    producer.flush()





    return jsonify({

        "message":
        "스캔 이벤트 전송 완료",


        "barcode":
        barcode,


        "product":
        product

    })
