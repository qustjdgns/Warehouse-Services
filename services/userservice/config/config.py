import os


class Config:

    SERVICE_NAME = os.getenv(
        "SERVICE_NAME",
        "SmartWMS UserService"
    )


    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "smartwms-secret-key"
    )



    # PostgreSQL

    DB_HOST = os.getenv(
        "DB_HOST",
        "localhost"
    )

    DB_USER = os.getenv(
        "DB_USER",
        "smartwms_user"
    )

    DB_PASSWORD = os.getenv(
        "DB_PASSWORD",
        "1234"
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "smartwms"
    )



    # Redis

    REDIS_HOST = os.getenv(
        "REDIS_HOST",
        "localhost"
    )

    REDIS_PORT = int(
        os.getenv(
            "REDIS_PORT",
            6379
        )
    )



    # Kafka

    KAFKA_HOST = os.getenv(
        "KAFKA_HOST",
        "localhost:9092"
    )



    # Flask

    DEBUG = os.getenv(
        "DEBUG",
        "false"
    ).lower() == "true"
