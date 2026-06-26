from flask import Blueprint, jsonify
from config.config import Config

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    # Kubernetes가 Pod 상태를 확인할 때 사용할 API
    return jsonify({
        "status": "ok",
        "service": Config.SERVICE_NAME
    })


@health_bp.route("/version", methods=["GET"])
def version():
    # GitLab CI/CD 배포 후 현재 실행 중인 버전을 확인할 API
    return jsonify({
        "service": Config.SERVICE_NAME,
        "version": Config.APP_VERSION,
        "env": Config.APP_ENV
    })
