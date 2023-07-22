from flask import Flask
from .extensions import db
from .routes.main import main
from .routes.admin import admin
from .models import AdminTable
from datetime import timedelta
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.permanent_session_lifetime = timedelta(minutes=30)
 
    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app