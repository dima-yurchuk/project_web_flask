from flask import Blueprint

api_bp = Blueprint('api_bp_in', __name__, template_folder="templates/task")

from . import view