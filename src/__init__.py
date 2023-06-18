from flask import Flask


def create_app():
    app = Flask(__name__)

    # register all routers-blueprints here
    from .api.auth import auth as auth_blueprint
    from .api.test_cases import test_cases as test_cases_blueprint
    from .api.test_suites import test_suites as test_suites_blueprint
    from .api.test_runs import test_runs as test_runs_blueprint
    from .api.projects import projects as projects_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(test_cases_blueprint, url_prefix='/test_cases')
    app.register_blueprint(test_suites_blueprint, url_prefix='/test_suites')
    app.register_blueprint(test_runs_blueprint, url_prefix='/test_runs')
    app.register_blueprint(projects_blueprint, url_prefix='/projects')

    return app
