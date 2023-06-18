from flask import Blueprint

test_suites = Blueprint('test_suites', __name__)


@test_suites.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


from . import views
