from flask import Blueprint

user_bp = Blueprint('user_bp_in', __name__, template_folder="templates/profile")

from . import view