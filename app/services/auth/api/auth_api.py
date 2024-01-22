from app.services.auth.api.api_exec import (registration_user, authenticate_user, refresh_token, refresh_guest_token,
                                            logout_func, get_user_data)
from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required

auth_api = Blueprint('users_api', __name__, url_prefix='/users')


@auth_api.route('/sign-up', methods=["POST"])
def add_new_user_api():
    resp_obj = registration_user(request.json)
    return resp_obj


@auth_api.route('/sign-in', methods=["POST"])
def user_auth_api():
    resp_obj = authenticate_user(request.json)
    return resp_obj


@auth_api.route('/refresh-guest-token', methods=["GET"])
def user_guest_refresh_token_api():
    return refresh_guest_token()


@auth_api.route('/refresh-token', methods=["GET"])
@jwt_required(refresh=True)
def user_refresh_token_api():
    return refresh_token()


@auth_api.route('/current-user', methods=["GET"])
@jwt_required(refresh=True)
def user_data_get():
    return get_user_data()


@auth_api.route('/logout', methods=["POST"])
@jwt_required()
def user_logout_api():
    return logout_func()
