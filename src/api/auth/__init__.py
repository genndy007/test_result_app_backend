from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


from . import views
