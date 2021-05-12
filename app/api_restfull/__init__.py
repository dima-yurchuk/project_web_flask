from flask import Blueprint

api_restfull_bp = Blueprint('api_restfull_bp_in', __name__, template_folder="templates/task")

from . import view