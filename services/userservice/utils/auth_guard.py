from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    # 로그인하지 않은 사용자는 로그인 페이지로 이동
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect("/login-page")

        return func(*args, **kwargs)

    return wrapper


def role_required(role):
    # 특정 role만 접근 허용
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "username" not in session:
                return redirect("/login-page")

            if session.get("role") != role:
                return redirect("/login-page")

            return func(*args, **kwargs)

        return wrapper

    return decorator
