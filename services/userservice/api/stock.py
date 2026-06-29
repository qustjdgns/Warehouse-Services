from flask import Blueprint, request, jsonify
from services.product_service import inbound_stock, outbound_stock

stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/stock/in", methods=["POST"])
def stock_in():
    data = request.get_json()

    barcode = data.get("barcode")
    quantity = int(data.get("quantity", 0))

    if quantity <= 0:
        return jsonify({"error": "입고 수량은 1 이상이어야 합니다."}), 400

    success, message, product = inbound_stock(barcode, quantity)

    if not success:
        return jsonify({"error": message}), 400

    return jsonify({
        "message": message,
        "barcode": barcode,
        "quantity": quantity,
        "product": product
    })


@stock_bp.route("/stock/out", methods=["POST"])
def stock_out():
    data = request.get_json()

    barcode = data.get("barcode")
    quantity = int(data.get("quantity", 0))

    if quantity <= 0:
        return jsonify({"error": "출고 수량은 1 이상이어야 합니다."}), 400

    success, message, product = outbound_stock(barcode, quantity)

    if not success:
        return jsonify({"error": message, "product": product}), 400

    return jsonify({
        "message": message,
        "barcode": barcode,
        "quantity": quantity,
        "product": product
    })
