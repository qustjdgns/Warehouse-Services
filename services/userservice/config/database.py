import pymysql


def get_connection():
    # Flask 서비스에서 MariaDB에 접속할 때 사용하는 공통 연결 함수
    return pymysql.connect(
        host="localhost",
        user="smartwms_user",
        password="1234",
        database="smartwms",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
