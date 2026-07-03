from flask import Blueprint, jsonify, request
from config.database import get_connection

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, full_name, role
                FROM users
                ORDER BY id
            """)
            return jsonify(cursor.fetchall())

    finally:
        conn.close()


@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    full_name = data.get("full_name")
    role = data.get("role")

    if not username or not password or not full_name or not role:
        return jsonify({"error": "모든 값을 입력하세요."}), 400

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, password, full_name, role)
                VALUES (%s, %s, %s, %s)
            """, (username, password, full_name, role))

        conn.commit()
        return jsonify({"message": "사용자 등록 완료"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    full_name = data.get("full_name")
    role = data.get("role")
    password = data.get("password")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            if password:
                cursor.execute("""
                    UPDATE users
                    SET full_name=%s, role=%s, password=%s
                    WHERE id=%s
                """, (full_name, role, password, user_id))
            else:
                cursor.execute("""
                    UPDATE users
                    SET full_name=%s, role=%s
                    WHERE id=%s
                """, (full_name, role, user_id))

        conn.commit()
        return jsonify({"message": "사용자 수정 완료"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))

        conn.commit()
        return jsonify({"message": "사용자 삭제 완료"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()
