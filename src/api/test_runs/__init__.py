from flask import Blueprint

test_runs = Blueprint('test_runs', __name__)

from . import views
