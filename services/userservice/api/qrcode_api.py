# 상품 QR 이미지와 QR 라벨 페이지 API

from flask import Blueprint, send_file, render_template
from io import BytesIO
import qrcode
from services.product_service import get_product

qrcode_bp = Blueprint("qrcode", __name__)


@qrcode_bp.route("/products/<barcode>/qrcode", methods=["GET"])
def product_qrcode(barcode):
    # QR에는 상품 barcode 값만 저장
    img = qrcode.make(barcode)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")


@qrcode_bp.route("/products/<barcode>/qrcode-label", methods=["GET"])
def product_qrcode_label(barcode):
    # 상품 정보 조회
    product = get_product(barcode)

    if product is None:
        return "상품을 찾을 수 없습니다.", 404

    return render_template(
        "qrcode_label.html",
        product=product
    )
