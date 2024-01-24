import pytz
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from app.utils.utils import to_dict_func
import uuid
from datetime import datetime
from app.db import db


class Users(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    name = Column(String(255))
    surname = Column(String(255))
    second_name = Column(String(255))
    image_logo = Column(String(2000))
    date_create = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    date_update = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    source = Column(Integer)
    role = Column(Integer, nullable=False)

    def to_dict(self):
        return to_dict_func(self)


class UserRole(db.Model):
    __tablename__ = "user_role"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255))
    priority = Column(Integer)
    code = Column(String(255))
    date_create = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    date_update = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    source = Column(Integer)

    def to_dict(self):
        return to_dict_func(self)


class Phones(db.Model):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone_number = Column(String(100), index=True)
    date_create = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    date_update = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    source = Column(Integer)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return to_dict_func(self)


class Emails(db.Model):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String(500), index=True)
    date_create = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    date_update = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    source = Column(Integer)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return to_dict_func(self)


class Address(db.Model):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String(500))
    date_create = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    date_update = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    source = Column(Integer)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return to_dict_func(self)


class Password(db.Model):
    __tablename__ = "password"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    password_hash = Column(String(500))
    date_create = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    date_update = Column(DateTime, default=datetime.now(tz=pytz.UTC))
    source = Column(Integer)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        return to_dict_func(self)
