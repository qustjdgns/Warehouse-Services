from flask import Blueprint, jsonify
from config.database import get_connection

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def get_history():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT
                    h.id,
                    h.barcode,
                    p.name AS product_name,
                    h.type,
                    h.quantity,
                    h.worker,
                    DATE_FORMAT(h.created_at, '%Y-%m-%d %H:%i:%s') AS created_at
                FROM history h
                LEFT JOIN products p ON h.barcode = p.barcode
                ORDER BY h.created_at DESC
            """
            cursor.execute(sql)
            return jsonify(cursor.fetchall())

    finally:
        conn.close()
