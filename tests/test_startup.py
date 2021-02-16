import os
import tempfile

import pytest

from umba_assessment_flask import create_app


@pytest.fixture
def client():
    db_fd, create_app.app.config['DATABASE'] = tempfile.mkstemp()
    create_app.app.config['TESTING'] = True

    with create_app.app.test_client() as client:
        with create_app.app.app_context():
            create_app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(create_app.app.config['DATABASE'])