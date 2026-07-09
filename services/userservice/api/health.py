from flask import Blueprint, jsonify

from config.database import get_connection
from config.redis import redis_client

from config.kafka import create_producer



health_bp = Blueprint(
    "health",
    __name__
)





@health_bp.route(
    "/health",
    methods=["GET"]
)
def health():


    result = {

        "service":
        "SmartWMS UserService",

        "status":
        "running"

    }



    # PostgreSQL 확인

    try:

        conn = get_connection()

        conn.close()


        result["postgresql"] = "ok"


    except Exception:


        result["postgresql"] = "error"





    # Redis 확인

    try:

        redis_client.ping()

        result["redis"] = "ok"


    except Exception:


        result["redis"] = "error"





    # Kafka 확인

    try:

        producer = create_producer()

        producer.close()


        result["kafka"] = "ok"


    except Exception:


        result["kafka"] = "error"





    return jsonify(
        result
    )
