from flask import Blueprint, jsonify

from config.redis import redis_client

import json



notifications_bp = Blueprint(
    "notifications",
    __name__
)





@notifications_bp.route(
    "/notifications",
    methods=["GET"]
)
def get_notifications():


    key = "notifications:low-stock"



    data = redis_client.get(
        key
    )



    if data is None:

        return jsonify([])



    return jsonify(
        json.loads(data)
    )
