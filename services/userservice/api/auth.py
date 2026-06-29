from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

# 임시 사용자 데이터(Mock Data)
USERS = {
    "manager": {
        "password": "1234",
        "role": "manager"
    },
    "operator": {
        "password": "1234",
        "role": "operator"
    }
}


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = USERS.get(username)

    if user is None:
        return jsonify({"error": "존재하지 않는 사용자입니다."}), 401

    if user["password"] != password:
        return jsonify({"error": "비밀번호가 올바르지 않습니다."}), 401

    return jsonify({
        "message": "로그인 성공",
        "username": username,
        "role": user["role"]
    })
