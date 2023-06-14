from flask import Blueprint

test_suites = Blueprint('test_suites', __name__)

from . import views
