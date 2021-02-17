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

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    if username != None:
        users = db.get_single_user(username)
    else:
        total, users = db.get_all_profiles(offset=offset, per_page=per_page)



    return jsonify([dict(ix) for ix in users])
