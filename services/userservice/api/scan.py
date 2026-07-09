from flask import Blueprint, request, jsonify
from services.scan_service import validate_barcode
from services.product_service import get_product

from kafka import KafkaProducer
import json


scan_bp = Blueprint("scan", __name__)


# Kafka Producer 설정
producer = KafkaProducer(
    bootstrap_servers=["kafka-service:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


@scan_bp.route("/scan", methods=["POST"])
def scan():

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "JSON body가 필요합니다."
        }), 400


    barcode = data.get("barcode")


    # barcode 검증
    is_valid, message = validate_barcode(barcode)

    if not is_valid:
        return jsonify({
            "error": message
        }), 400


    # 상품 조회
    product = get_product(barcode)

    if product is None:
        return jsonify({
            "error": "상품을 찾을 수 없습니다."
        }), 404


    # Kafka 이벤트 발행
    event = {
        "event_type": "SCAN",
        "barcode": barcode,
        "product": product
    }


    producer.send(
        "scan-event",
        event
    )


    producer.flush()


    return jsonify({
        "message": "스캔 이벤트 발행 완료",
        "barcode": barcode,
        "product": product
    })
