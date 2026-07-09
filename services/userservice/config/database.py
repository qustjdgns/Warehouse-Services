import psycopg
from psycopg.rows import dict_row


def get_connection():

    return psycopg.connect(
        host="postgres-service",
        user="smartwms_user",
        password="1234",
        dbname="smartwms",
        row_factory=dict_row
    )
