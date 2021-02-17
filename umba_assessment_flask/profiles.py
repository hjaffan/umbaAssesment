from flask import (
    Blueprint, jsonify, request
)

from flask_paginate import get_page_args

from umba_assessment_flask import db

bp = Blueprint('profiles', __name__, url_prefix='/profiles')


# TODO: Implement a JSON response call with pagination
@bp.route('/', methods=['GET'])
def home():
    username = request.args.get('user')
    offset = 0
    per_page = 100
    if request.args.get('offset'):
        offset = int(request.args.get('offset'))

    if username is not None:
        users = db.get_single_user(username)
    else:
        total, users = db.get_all_profiles(offset=offset, per_page=per_page)
    final_users = []
    for user in users:
        us = {"id": user[0], "username": str(user[1]).strip(), "profile_url": user[2], "type": str(user[3]).strip(),
              "profile": user[4]}
        final_users.append(us)
    return jsonify(final_users)
