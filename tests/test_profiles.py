import os
import tempfile

import pytest

import umba_assessment_flask


@pytest.fixture
def client():
    db_fd, umba_assessment_flask.create_app.app.config['DATABASE'] = tempfile.mkstemp()
    umba_assessment_flask.create_app.app.config['TESTING'] = True

    with umba_assessment_flask.create_app.app.test_client() as client:
        with umba_assessment_flask.create_app.app.app_context():
            umba_assessment_flask.create_app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(umba_assessment_flask.create_app.app.config['DATABASE'])

