import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')

    database_path = os.path.join(app.instance_path, os.getenv('DB_NAME', '../instance/test.db'))
    github_auth_token = os.getenv('GITHUB_AUTH_TOKEN')
    number_of_users = os.getenv('NUMBER_OF_USERS', 150)
    per_page = os.getenv('PER_PAGE', 25)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=database_path,
        GITHUB_AUTH_KEY=github_auth_token,
        NUMBER_OF_USERS=number_of_users,
        PER_PAGE=per_page
    )

    if test_config is None:
        from umba_assessment_flask import db
        # load the instance config, if it exists, when not testing

        db.init_db(github_auth_token, database_path, number_of_users)
        app.config.from_pyfile('config.py', silent=True)

        if github_auth_token == "":
            print("Github Auth Token not provided")
            # raise
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from umba_assessment_flask import home
    from umba_assessment_flask import profiles

    app.register_blueprint(profiles.bp)
    app.register_blueprint(home.bp)

    return app
