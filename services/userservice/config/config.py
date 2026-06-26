import os


class Config:
    # 서비스 이름
    SERVICE_NAME = os.getenv("SERVICE_NAME", "userservice")

    # 배포 버전
    APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")

    # 실행 환경: local, dev, prod
    APP_ENV = os.getenv("APP_ENV", "local")

    # 나중에 연결할 WMS Server 주소
    WMS_SERVER_URL = os.getenv("WMS_SERVER_URL", "http://wms-service:5001")
