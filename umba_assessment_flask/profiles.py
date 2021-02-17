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
    offset = request.args.get('offset')
    per_page = request.args.get('per_page')

    if int(per_page) > 100:
        per_page = 100

    if username is not None:
        users = db.get_single_user(username)
    else:
        total, users = db.get_all_profiles(offset=offset, per_page=per_page)
    final_users = []
    for user in users:
        us = {"username": user[0], "id": user[1], "image_url": user[2]}
        final_users.append(us)
    return jsonify(final_users)
