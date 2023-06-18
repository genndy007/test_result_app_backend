from flask import Blueprint

projects = Blueprint('projects', __name__)


@projects.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


from . import views
