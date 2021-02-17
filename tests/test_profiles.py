import os
import tempfile
import json
import pytest

import umba_assessment_flask


def test_profile(client):
    rv = client.get('/profiles', follow_redirects=True)

    data = json.loads(rv.data)

    assert data[0]['USERNAME'] == "user1"
    assert len(data) == 10


def test_profile_search_user(client):
    rv = client.get('/profiles?user=user5', follow_redirects=True)

    data = json.loads(rv.data)

    assert data[0]['USERNAME'] == "user5"
    assert len(data) == 1