from flask import Flask


def create_app():
    app = Flask(__name__)

    # register all routers-blueprints here
    from .api.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
