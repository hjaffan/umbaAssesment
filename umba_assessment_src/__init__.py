import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    # TODO: Fail the application if GITHUB_AUTH_TOKEN not found
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, os.getenv('DB_NAME', '../instance/test.db')),
        GITHUB_AUTH_KEY=os.getenv('GITHUB_AUTH_TOKEN'),
        NUMBER_OF_USERS=os.getenv('NUMBER_OF_USERS', 150),
        PER_PAGE=os.getenv('PER_PAGE', 25)
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from . import profiles, home, startup
    app.register_blueprint(startup.bp)
    app.register_blueprint(profiles.bp)
    app.register_blueprint(home.bp)

    return app
