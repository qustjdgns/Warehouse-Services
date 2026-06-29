from flask import Flask, jsonify, render_template
from config.config import Config
from api.health import health_bp
from api.scan import scan_bp
from api.auth import auth_bp
from api.stock import stock_bp

def create_app():
    # Flask 애플리케이션 생성
    app = Flask(__name__)

    # 설정 적용
    app.config.from_object(Config)

    # API Blueprint 등록
    app.register_blueprint(health_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)

    @app.route("/", methods=["GET"])
    def home():
        # 기본 서비스 확인용 API
        return jsonify({
            "service": Config.SERVICE_NAME,
            "message": "SmartWMS UserService is running"
        })

    @app.route("/pda", methods=["GET"])
    def pda():
        # 스마트폰/PDA 카메라 스캔 화면
        return render_template("pda.html")

    @app.route("/login-page", methods=["GET"])
    def login_page():
        return render_template("login.html")

    @app.route("/operator/home", methods=["GET"])
    def operator_home():
        return render_template("operator_home.html")

    @app.route("/manager/dashboard", methods=["GET"])
    def manager_dashboard():
        return render_template("manager_dashboard.html")

    return app


app = create_app()


if __name__ == "__main__":
    # 0.0.0.0은 Docker/Kubernetes 환경에서 외부 접속을 위해 필요
    app.run(host="0.0.0.0", port=5000, debug=True)
