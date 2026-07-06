from flask import Blueprint, jsonify, request, session
from config.database import get_connection

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings/me", methods=["GET"])
def get_my_profile():
    username = session.get("username")

    if not username:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT username, full_name, role
                FROM users
                WHERE username = %s
            """, (username,))
            return jsonify(cursor.fetchone())

    finally:
        conn.close()


@settings_bp.route("/settings/profile", methods=["PUT"])
def update_profile():
    username = session.get("username")
    data = request.get_json()
    full_name = data.get("full_name")

    if not username:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    if not full_name:
        return jsonify({"error": "Full Name을 입력하세요."}), 400

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET full_name = %s
                WHERE username = %s
            """, (full_name, username))

        conn.commit()
        session["full_name"] = full_name

        return jsonify({
            "message": "프로필 수정 완료",
            "full_name": full_name
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()


@settings_bp.route("/settings/password", methods=["PUT"])
def update_password():
    username = session.get("username")
    data = request.get_json()

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not username:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    if not current_password or not new_password:
        return jsonify({"error": "현재 비밀번호와 새 비밀번호를 입력하세요."}), 400

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT password
                FROM users
                WHERE username = %s
            """, (username,))
            user = cursor.fetchone()

            if user is None:
                return jsonify({"error": "사용자를 찾을 수 없습니다."}), 404

            if user["password"] != current_password:
                return jsonify({"error": "현재 비밀번호가 올바르지 않습니다."}), 400

            cursor.execute("""
                UPDATE users
                SET password = %s
                WHERE username = %s
            """, (new_password, username))

        conn.commit()

        return jsonify({"message": "비밀번호 변경 완료"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()

@settings_bp.route("/settings/account", methods=["DELETE"])
def delete_my_account():
    username = session.get("username")
    role = session.get("role")

    if not username:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # 마지막 Manager 삭제 방지
            if role == "manager":
                cursor.execute("""
                    SELECT COUNT(*) AS manager_count
                    FROM users
                    WHERE role = 'manager'
                """)
                manager_count = cursor.fetchone()["manager_count"]

                if manager_count <= 1:
                    return jsonify({
                        "error": "마지막 Manager 계정은 탈퇴할 수 없습니다."
                    }), 400

            cursor.execute("""
                DELETE FROM users
                WHERE username = %s
            """, (username,))

        conn.commit()
        session.clear()

        return jsonify({"message": "회원 탈퇴 완료"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()
