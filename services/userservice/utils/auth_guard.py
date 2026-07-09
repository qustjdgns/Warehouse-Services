from functools import wraps

from flask import session, jsonify



def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):


        if "username" not in session:


            return jsonify({

                "error":
                "로그인이 필요합니다."

            }),401



        return func(*args, **kwargs)



    return wrapper






def role_required(role):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):


            user_role = session.get(
                "role"
            )



            if user_role != role:


                return jsonify({

                    "error":
                    "권한이 없습니다."

                }),403



            return func(*args, **kwargs)



        return wrapper


    return decorator
