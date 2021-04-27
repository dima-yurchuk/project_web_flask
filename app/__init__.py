from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


# app = Flask(__name__)
# app.config.from_object('config')
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view='user_bp_in.login'
login_manager.login_message_category='info'

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    with app.app_context():
        app.config.from_object('config')
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        from .profile import user_bp
        from .task import task_bp
        from .contact_form import contact_form_bp
        from . import view
        app.register_blueprint(user_bp, url_prefix='/auth')
        app.register_blueprint(task_bp, url_prefix='/tasks_bp')
        app.register_blueprint(contact_form_bp, url_prefix='')


        from .profile import create_module as admin_create_module
        admin_create_module(app)
        # initialize_extensions(app)
        # register_blueprints(app)
    return app
