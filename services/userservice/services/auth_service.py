from config.database import get_connection



def login_user(data):

    username = data.get(
        "username"
    )

    password = data.get(
        "password"
    )


    conn = get_connection()


    try:

        with conn.cursor() as cursor:


            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    full_name,
                    role
                FROM users
                WHERE username = %s
                AND password = %s
                """,
                (
                    username,
                    password
                )
            )


            user = cursor.fetchone()



            if user is None:

                return False, None



            return True, user



    finally:

        conn.close()





def register_user(data):


    username = data.get(
        "username"
    )

    password = data.get(
        "password"
    )

    full_name = data.get(
        "full_name"
    )

    role = data.get(
        "role",
        "operator"
    )



    conn = get_connection()



    try:


        with conn.cursor() as cursor:


            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password,
                    full_name,
                    role
                )
                VALUES
                (%s,%s,%s,%s)
                """,
                (
                    username,
                    password,
                    full_name,
                    role
                )
            )


        conn.commit()


        return True, "회원가입 완료"



    except Exception as e:


        conn.rollback()

        return False, str(e)



    finally:

        conn.close()
