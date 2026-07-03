from flask import Blueprint, jsonify
from config.database import get_connection

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/notifications", methods=["GET"])
def get_notifications():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            notifications = []

            # 재고 부족 알림
            cursor.execute("""
                SELECT barcode, name, stock
                FROM products
                WHERE stock <= 5
                ORDER BY stock ASC
                LIMIT 5
            """)
            low_stock_products = cursor.fetchall()

            for item in low_stock_products:
                notifications.append({
                    "type": "warning",
                    "title": "Low Stock",
                    "message": f"{item['name']} 재고 {item['stock']} EA",
                    "barcode": item["barcode"]
                })
            return jsonify(notifications)

    finally:
        conn.close()
