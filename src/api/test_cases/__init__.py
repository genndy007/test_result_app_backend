from flask import Blueprint

test_cases = Blueprint('test_cases', __name__)

from . import views
