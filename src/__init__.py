from flask import Flask


def create_app():
    app = Flask(__name__)

    # register all routers-blueprints here
    from .api.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api.test_cases import test_cases as test_cases_blueprint
    app.register_blueprint(test_cases_blueprint, url_prefix='/test_cases')

    return app
