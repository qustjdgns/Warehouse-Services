import os
import psycopg
from psycopg.rows import dict_row


def get_connection():

    return psycopg.connect(

        host=os.getenv(
            "DB_HOST",
            "localhost"
        ),

        user=os.getenv(
            "DB_USER",
            "smartwms_user"
        ),

        password=os.getenv(
            "DB_PASSWORD",
            "1234"
        ),

        dbname=os.getenv(
            "DB_NAME",
            "smartwms"
        ),

        row_factory=dict_row
    )
