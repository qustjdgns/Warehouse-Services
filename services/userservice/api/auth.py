from flask import Blueprint, request, jsonify, session
from services.auth_service import get_user_by_username

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    # 사용자가 보낸 JSON 데이터 받기
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # DB에서 사용자 조회
    user = get_user_by_username(username)

    if user is None:
        return jsonify({
            "error": "존재하지 않는 사용자입니다."
        }), 401

    # 현재는 실습용이라 평문 비밀번호 비교
    if user["password"] != password:
        return jsonify({
            "error": "비밀번호가 올바르지 않습니다."
        }), 401

    # 로그인 사용자 정보 저장
    session["username"] = user["username"]
    session["role"] = user["role"]

    return jsonify({
        "message": "로그인 성공",
        "username": user["username"],
        "role": user["role"]
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():
    # 로그인 정보 삭제
    session.clear()

    return jsonify({
        "message": "로그아웃 완료"
    })
