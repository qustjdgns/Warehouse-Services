from config.database import get_connection


def get_user_by_username(username):
    # username으로 사용자 1명 조회
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, username, password, role
                FROM users
                WHERE username = %s
            """
            cursor.execute(sql, (username,))
            return cursor.fetchone()

    finally:
        conn.close()
