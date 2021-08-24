import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from toDoItems.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view='users.login'
login_manager.login_message = 'Please login to access the request page'
login_manager.login_message_category = 'info'
mail = Mail()


# Application factory (Factory function)
def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from toDoItems.main.routes import main
    from toDoItems.users.routes import users
    from toDoItems.items.routes import items
    from toDoItems.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(items)
    app.register_blueprint(errors)

    return app


