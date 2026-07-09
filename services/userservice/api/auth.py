from flask import Blueprint, request, jsonify, session
from services.auth_service import login_user, register_user

import redis
import os
import json


auth_bp = Blueprint(
    "auth",
    __name__
)


redis_client = redis.Redis(
    host=os.getenv(
        "REDIS_HOST",
        "localhost"
    ),
    port=6379,
    decode_responses=True
)



@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "JSON 데이터가 필요합니다."
        }),400



    success, message = register_user(data)



    if not success:

        return jsonify({
            "error": message
        }),400



    return jsonify({
        "message": message
    })





@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "JSON 데이터가 필요합니다."
        }),400



    success, user = login_user(data)



    if not success:

        return jsonify({
            "error": "로그인 실패"
        }),401



    session["username"] = user["username"]

    session["full_name"] = user.get(
        "full_name",
        user["username"]
    )



    session_key = f"session:{user['username']}"



    redis_client.set(

        session_key,

        json.dumps(user),

        ex=3600

    )



    return jsonify({

        "message": "로그인 성공",

        "user": user

    })





@auth_bp.route(
    "/logout",
    methods=["POST"]
)
def logout():


    username = session.get(
        "username"
    )


    if username:


        redis_client.delete(

            f"session:{username}"

        )



    session.clear()



    return jsonify({

        "message":
        "로그아웃 완료"

    })
