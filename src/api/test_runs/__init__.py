from flask import Blueprint

test_runs = Blueprint('test_runs', __name__)


@test_runs.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

from . import views
