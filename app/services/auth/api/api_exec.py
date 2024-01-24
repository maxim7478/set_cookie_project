from flask_jwt_extended import (create_access_token,
                                create_refresh_token, get_jwt_identity, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies, get_jwt
                                )
from flask import jsonify, make_response
import logging

from app.db import db
from app.services.auth.models.models import Password, Emails, Users
from app.services.auth.helpers.oauth_utils import get_user_by_email, verify_password, hash_password, get_user_by_id


def authenticate_user(form_data):
    user_email = form_data["email"]
    user_password = form_data["password"]

    status = 200
    response_obj = {
        "status": status,
        "message": "",
        "data": {},
    }
    try:
        user = get_user_by_email(user_email)
        if user is None:
            logging.error(f'User log in error: user don`t exist')
            status = 400
            response_obj = {
                "status": status,
                "message": "Email or password are not correct",
                "data": {},
            }
            return response_obj, status
        password_hash = Password.query.filter(Password.user_id == user["id"]).first()
        if not verify_password(user_password, password_hash.password_hash):
            logging.error(f'User log in error: password is not correct')
            status = 400
            response_obj = {
                "status": status,
                "message": "Email or password are not correct",
                "data": {},
            }
            return response_obj, status

        jwt_claims = {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"]
        }

        # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=jwt_claims)
        token_refresh = create_refresh_token(identity=jwt_claims)
        response_obj["data"] = user
        response_obj["message"] = "Log in is successful"
        resp_obj = make_response(response_obj)
        set_access_cookies(resp_obj, access_token)
        set_refresh_cookies(resp_obj, token_refresh)
        return resp_obj, status
    except Exception as ex:
        status = 400
        response_obj = {
            "status": status,
            "message": str(ex)
        }
        logging.error(f'User log in error: {ex}')
        return response_obj, status


def refresh_token():
    status = 200
    response_obj = {
        "status": status,
        "message": "Token is refreshed successful"
    }
    resp_obj = None
    try:
        identity = get_jwt_identity()

        new_access_token = create_access_token(identity=identity)
        new_refresh_token = create_refresh_token(identity=identity)
        resp_obj = make_response(response_obj)
        set_access_cookies(resp_obj, new_access_token)
        set_refresh_cookies(resp_obj, new_refresh_token)
        logging.info('Token is refreshed successful')
    except Exception as ex:
        status = 400
        response_obj["message"] = "Something wrong"
        response_obj["status"] = status
        resp_obj = make_response(response_obj)
        logging.error(f'Access token refresh error: {ex}')
    finally:
        return resp_obj, status


def refresh_guest_token():
    status = 200
    response_obj = {
        "status": status,
        "message": "Guest token is refreshed successful"
    }
    resp_obj = None
    try:
        new_access_token = create_access_token(identity='')
        resp_obj = make_response(response_obj)
        set_access_cookies(resp_obj, new_access_token)
        resp_obj.delete_cookie("refresh_token_cookie")
        logging.info('Guest token is refreshed successful')
    except Exception as ex:
        status = 400
        logging.error(f'Guest token refresh error: {ex}')
        response_obj["message"] = "Something wrong"
        response_obj["status"] = status
        resp_obj = make_response(response_obj)
    finally:
        return resp_obj, status


def registration_user(form_data):
    try:
        exist_email = Emails.query.filter(Emails.email == form_data["email"].lower()).first()
        if exist_email:
            status = 409
            response_obj = {
                "status": status,
                "message": "User exist"
            }
            logging.error(f'User added error: email exist')
            return response_obj, status

        if form_data["password"] != form_data["passwordConfirm"]:
            status = 409
            response_obj = {
                "status": status,
                "message": "Password and password confirm isn`t match"
            }
            logging.error(f'User added error: password and password don`t match')
            return response_obj, status

        form_data["password"] = hash_password(form_data["password"])
        del form_data["passwordConfirm"]

        new_user = Users()
        new_user.name = form_data["name"]
        new_user.surname = form_data["surname"]
        new_user.second_name = form_data["second_name"]
        new_user.source = ""
        new_user.is_active = True
        db.session.add(new_user)
        db.session.commit()

        new_password = Password()
        new_password.user_id = new_user.id
        new_password.password_hash = form_data["password"]

        db.session.add(new_password)
        db.session.commit()

        new_email = Emails()
        new_email.email = form_data["email"]
        new_email.user_id = new_user.id
        new_email.source = new_user.id
        new_email.is_active = True

        db.session.add(new_email)
        db.session.commit()

        current_user = new_user.to_dict()
        current_user['email'] = new_email.email

        status = 201
        response_obj = {
            "status": status,
            "message": "New user created",
            "data": current_user,
        }
        logging.info('User added success')
        return response_obj, status

    except Exception as ex:
        status = 400
        response_obj = {
            "status": status,
            "message": str(ex)
        }
        logging.error(f'User added error: {ex}')
        return response_obj, status


def logout_func():
    try:
        status = 200
        response_obj = {
            "status": status,
            "message": "Logout is successful",
        }
        resp_obj = make_response(response_obj)
        unset_jwt_cookies(resp_obj)
        new_access_token = create_access_token(identity='')
        set_access_cookies(resp_obj, new_access_token)
        logging.info('Logout is successful')
        return resp_obj, 200
    except Exception as ex:
        status = 400
        response_obj = {
            "status": status,
            "message": str(ex)
        }
        logging.error(f'Logout error: {ex}')
        return response_obj, status


def get_user_data():
    try:
        status = 200
        response_obj = {
            "status": status,
            "message": "Getting user is successful",
            "data": None
        }
        identity = get_jwt_identity()
        if identity and identity["id"]:
            user = get_user_by_id(identity["id"])
            response_obj["data"] = user
        return jsonify(response_obj), status
    except Exception as ex:
        status = 400
        response_obj = {
            "status": status,
            "message": str(ex)
        }
        logging.error(f'Getting user data error: {ex}')
        return response_obj, status
