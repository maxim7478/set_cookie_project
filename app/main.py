from flask import Flask, jsonify
from app.services.auth.api.auth_api import auth_api
from app.config import config
from app.db import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(app_cfg):
    app_flask = Flask(__name__)
    app_flask.config.from_object(app_cfg)

    db.init_app(app_flask)

    with app_flask.app_context():
        db.create_all()

    CORS(app_flask, headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)

    app_flask.register_blueprint(auth_api)

    jwt = JWTManager(app_flask)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_date):
        print(jwt_header)
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def expired_token_callback(error):
        print(error)
        return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def expired_token_callback(error):
        print(error)
        return jsonify({"message": "Request doesn`t contain valid token", "error": "authorization_header"}), 401

    return app_flask


app = create_app(config)


def run_app():
    app.run(debug=False, host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    run_app()




