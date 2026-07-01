from flask import Blueprint, jsonify, request
from services.product_service import (
    get_products,
    create_product,
    update_product,
    delete_product
)

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def products():
    # 상품 목록 조회
    return jsonify(get_products())


@products_bp.route("/products", methods=["POST"])
def add_product():
    # 상품 추가
    data = request.get_json()

    barcode = data.get("barcode")
    name = data.get("name")
    stock = int(data.get("stock", 0))
    location = data.get("location")

    if not barcode or not name or not location:
        return jsonify({"error": "barcode, name, location 값이 필요합니다."}), 400

    success, message = create_product(barcode, name, stock, location)

    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message})


@products_bp.route("/products/<barcode>", methods=["PUT"])
def edit_product(barcode):
    # 상품 수정
    data = request.get_json()

    name = data.get("name")
    stock = int(data.get("stock", 0))
    location = data.get("location")

    if not name or not location:
        return jsonify({"error": "name, location 값이 필요합니다."}), 400

    success, message = update_product(barcode, name, stock, location)

    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message})


@products_bp.route("/products/<barcode>", methods=["DELETE"])
def remove_product(barcode):
    # 상품 삭제
    success, message = delete_product(barcode)

    if not success:
        return jsonify({"error": message}), 400

    return jsonify({"message": message})
