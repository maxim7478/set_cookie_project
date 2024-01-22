from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

from app.config import config

SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URI


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)