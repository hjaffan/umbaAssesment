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
    page = 0
    per_page = 100
    offset = 0
    if request.args.get('page'):
        page = int(request.args.get('page'))
        offset = page * 100

    if username is not None:
        users = db.get_single_user(username)
        page_count = (len(users) / 100)
    else:
        total, users = db.get_all_profiles(offset=offset, per_page=per_page)
        page_count = int(total / 100)

    if page_count < 1:
        page_count = 0

    user_json = []
    for user in users:
        us = {"id": user[0], "username": str(user[1]).strip(), "avatar": user[2], "type": str(user[3]).strip(),
              "profile": str(user[4]).strip()}
        user_json.append(us)

    final_users = dict()
    final_users['page'] = page
    final_users['total_pages'] = page_count
    final_users['profiles'] = user_json
    return jsonify(final_users)
