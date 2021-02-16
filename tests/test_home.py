import os
import tempfile

import pytest

from umba_assessment_flask import create_app


# @pytest.fixture
# def client():
#     db_fd, create_app.app.config['DATABASE'] = tempfile.mkstemp()
#     create_app.app.config['TESTING'] = True
#
#     with create_app.app.test_client() as client:
#         with create_app.app.app_context():
#             create_app.init_db()
#         yield client
#
#     os.close(db_fd)
#     os.unlink(create_app.app.config['DATABASE'])


# We want to validate when home path is called. HTML page is displayed

def test_home(client):
    rv = client.get('/')

    # Assert All Users Display
    assert b'user1' in rv.data
    assert b'user2' in rv.data
    assert b'user3' in rv.data
    assert b'user4' in rv.data
    assert b'user5' in rv.data

    # Assert GitHub Profiles Display
    assert b'https://github.com/profiles/user1' in rv.data
    assert b'https://github.com/profiles/user2' in rv.data
    assert b'https://github.com/profiles/user3' in rv.data
    assert b'https://github.com/profiles/user4' in rv.data
    assert b'https://github.com/profiles/user5' in rv.data

