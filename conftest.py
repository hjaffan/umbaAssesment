import os
import tempfile

import pytest

from umba_assessment_flask import create_app
from umba_assessment_flask.db import get_db
from umba_assessment_flask.db import init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "tests/data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    github_auth_token = os.getenv('GITHUB_AUTH_TOKEN')
    # create the database and load test data
    with app.app_context():
        # init_db(github_auth_token)
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
