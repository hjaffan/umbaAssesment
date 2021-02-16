import sqlite3
import os
import pytest

from umba_assessment_flask.db import get_db, get_all_profiles


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_get_all_profiles(app):
    with app.app_context():

        count, users = get_all_profiles()

        assert count is 5
