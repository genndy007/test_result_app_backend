from flask import Blueprint

test_cases = Blueprint('test_cases', __name__)


@test_cases.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


from . import views
