import os
import tempfile
import json
import pytest

import umba_assessment_flask


def test_profile(client):
    rv = client.get('/profiles', follow_redirects=True)

    data = json.loads(rv.data)

    assert data['profiles'][0]['username'] == "user1"
    assert len(data['profiles']) == 10


def test_profile_search_user(client):
    rv = client.get('/profiles?user=user5', follow_redirects=True)

    data = json.loads(rv.data)

    assert data['profiles'][0]['username'] == "user5"
    assert len(data['profiles']) == 1