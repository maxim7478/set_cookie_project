from passlib.context import CryptContext
from app.services.auth.models.models import Emails, Users, Phones

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_user_by_email(email_str: str):
    current_user = None

    try:
        email = Emails.query.filter(Emails.email == email_str, Emails.is_active).first()
        if email is None:
            return None
        user = Users.query.filter(Users.id == email.user_id).first()
        if user is None:
            return None

        phone = Phones.query.filter(Phones.user_id == user.id, Phones.is_active).first()
        current_user = user.to_dict()
        current_user['email'] = email_str
        current_user['phone'] = phone.phone_number
    except Exception as ex:
        print(ex)
    finally:
        return current_user


def get_user_by_id(user_id: str):
    current_user = None
    try:
        user = Users.query.filter(Users.id == user_id).first()
        if user is None:
            return None
        email = Emails.query.filter(Emails.user_id == user.id and Emails.is_active).first()
        if email is None:
            return None
        current_user = user.to_dict()
        current_user['email'] = email.email
    except Exception as ex:
        print(ex)
    finally:
        return current_user
