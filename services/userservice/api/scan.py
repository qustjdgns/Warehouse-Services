from flask import Blueprint, request, jsonify

from services.scan_service import validate_barcode
from services.product_service import get_product

from config.kafka import create_producer



scan_bp = Blueprint(
    "scan",
    __name__
)



producer = create_producer()



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



    is_valid, message = validate_barcode(
        barcode
    )



    if not is_valid:

        return jsonify({

            "error":
            message

        }),400




    product = get_product(
        barcode
    )



    if product is None:

        return jsonify({

            "error":
            "상품을 찾을 수 없습니다."

        }),404




    event = {


        "event_type":
        "STOCK_UPDATE",


        "barcode":
        barcode,


        "quantity":
        data.get(
            "quantity",
            1
        ),


        "action":
        data.get(
            "action",
            "OUT"
        )

    }



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
