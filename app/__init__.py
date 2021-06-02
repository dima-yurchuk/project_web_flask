from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
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
        if os.environ.get('DATABASE_URL') is None: # for local work
            app.config.update(SQLALCHEMY_DATABASE_URI = 'sqlite:///form.db', SECRET_KEY = 'asfdsfsaaffdf')
        else: # for heroku work
            app.config.from_object('config')
        print(os.environ.get('DATABASE_URL'))
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        from .profile import user_bp
        from .task import task_bp
        from .contact_form import contact_form_bp
        from .api import api_bp
        from .api_restfull import api_restfull_bp
        from .swagger import swagger_bp
        from . import view
        app.register_blueprint(user_bp, url_prefix='/auth')
        app.register_blueprint(task_bp, url_prefix='/tasks_bp')
        app.register_blueprint(contact_form_bp, url_prefix='')
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(api_restfull_bp, url_prefix='/api/v2')
        app.register_blueprint(swagger_bp, url_prefix='/swagger')

        from .profile import create_module as admin_create_module
        admin_create_module(app)
        # initialize_extensions(app)
        # register_blueprints(app)
    return app
