# This code is importing various modules and classes needed for the Flask application.
from flask import Flask
from .extensions import db
from .routes.main import main
from .routes.admin import admin
from datetime import timedelta
from .config import Config


def create_app(config_class=Config):
    """
    The function creates and configures a Flask application with a specified configuration class,
    initializes the database, registers blueprints for different parts of the application, and creates
    the necessary database tables.
    
    :param config_class: The `config_class` parameter is used to specify the configuration class for the
    Flask application. The configuration class contains various settings and options for the
    application, such as database connection details, secret keys, and other environment-specific
    configurations
    :return: an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.permanent_session_lifetime = timedelta(minutes=30)
 
    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app