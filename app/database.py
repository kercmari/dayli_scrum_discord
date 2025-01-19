# app/database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        import app.models  # Importación explícita de modelos

        db.create_all()  # Crear tablas si no existen
