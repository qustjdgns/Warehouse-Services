from flask import Blueprint, request, jsonify
from services.scan_service import validate_barcode

scan_bp = Blueprint("scan", __name__)


@scan_bp.route("/scan", methods=["POST"])
def scan():
    # 사용자가 보낸 JSON 데이터 받기
    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "JSON body가 필요합니다."
        }), 400

    # barcode 값 추출
    barcode = data.get("barcode")

    # barcode 값 검증
    is_valid, message = validate_barcode(barcode)

    if not is_valid:
        return jsonify({
            "error": message
        }), 400

    # 지금은 WMS Server 연동 전이라 임시 응답 반환
    return jsonify({
        "message": "스캔 성공",
        "barcode": barcode,
        "next": "WMS Server로 서비스 요청 전달 예정"
    })
