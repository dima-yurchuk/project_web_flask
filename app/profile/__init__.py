from flask import Blueprint
from flask_admin import Admin

user_bp = Blueprint('user_bp_in', __name__, template_folder="templates/profile")

from .view import MyAdminIndexView
import warnings


admin = Admin(index_view=view.MyAdminIndexView())
def create_module(app, **kwargs):
    from .view import CustomView, UserModelView, CustomFileAdmin
    from .models import User
    from .. import db
    # admin = Admin(index_view=CustomView(), template_mode="bootstrap3")
    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CustomFileAdmin(app.static_folder, '/static/', name='Static Files'))
    # admin.add_view(UserAdminView(User, db.session, endpoint="users"))
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)

# user_bp = Blueprint('user_bp_in', __name__, template_folder="templates/profile")

from . import view