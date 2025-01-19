# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from .database import db, init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Inicializar DB
    init_db(app)

    # Configurar migraciones
    migrate = Migrate(app, db)

    from .routes import bp

    app.register_blueprint(bp)

    return app
