from flask import Flask, jsonify, render_template
from config.config import Config

from api.health import health_bp
from api.scan import scan_bp
from api.auth import auth_bp
from api.stock import stock_bp
from api.products import products_bp
from api.dashboard import dashboard_bp
from api.qrcode_api import qrcode_bp
from api.history import history_bp
from api.users import users_bp
from api.notifications import notifications_bp
from api.settings import settings_bp

from utils.auth_guard import role_required



def create_app():

    app = Flask(__name__)


    app.secret_key = Config.SECRET_KEY


    app.config.from_object(
        Config
    )



    # Blueprint 등록

    app.register_blueprint(
        health_bp
    )

    app.register_blueprint(
        scan_bp
    )

    app.register_blueprint(
        auth_bp
    )

    app.register_blueprint(
        stock_bp
    )

    app.register_blueprint(
        products_bp
    )

    app.register_blueprint(
        dashboard_bp
    )

    app.register_blueprint(
        qrcode_bp
    )

    app.register_blueprint(
        history_bp
    )

    app.register_blueprint(
        users_bp
    )

    app.register_blueprint(
        notifications_bp
    )

    app.register_blueprint(
        settings_bp
    )




    @app.route("/")
    def home():

        return jsonify({

            "service":
            Config.SERVICE_NAME,

            "message":
            "SmartWMS UserService is running"

        })




    @app.route(
        "/pda",
        methods=["GET"]
    )
    @role_required("operator")
    def pda():

        return render_template(
            "pda.html"
        )




    @app.route(
        "/login-page",
        methods=["GET"]
    )
    def login_page():

        return render_template(
            "login.html"
        )




    @app.route(
        "/operator/home",
        methods=["GET"]
    )
    @role_required("operator")
    def operator_home():

        return render_template(
            "operator_home.html"
        )




    @app.route(
        "/manager/dashboard",
        methods=["GET"]
    )
    @role_required("manager")
    def manager_dashboard():

        return render_template(
            "manager_dashboard.html"
        )




    @app.route(
        "/manager/products",
        methods=["GET"]
    )
    @role_required("manager")
    def manager_products():

        return render_template(
            "manager_products.html"
        )




    @app.route(
        "/manager/history",
        methods=["GET"]
    )
    @role_required("manager")
    def manager_history():

        return render_template(
            "manager_history.html"
        )




    @app.route(
        "/manager/inventory",
        methods=["GET"]
    )
    @role_required("manager")
    def manager_inventory():

        return render_template(
            "manager_inventory.html"
        )




    @app.route(
        "/manager/users",
        methods=["GET"]
    )
    @role_required("manager")
    def manager_users():

        return render_template(
            "manager_users.html"
        )




    @app.route(
        "/manager/settings",
        methods=["GET"]
    )
    @role_required("manager")
    def manager_settings():

        return render_template(
            "manager_settings.html"
        )





    @app.after_request
    def add_no_cache_headers(response):

        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, max-age=0"


        response.headers[
            "Pragma"
        ] = "no-cache"


        response.headers[
            "Expires"
        ] = "0"


        return response



    return app





app = create_app()



if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
