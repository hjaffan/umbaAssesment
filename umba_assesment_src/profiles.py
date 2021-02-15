import functools
import json
from flask import (
    Blueprint, render_template
)


from umba_assesment_src.db import get_all_profiles

bp = Blueprint('profiles', __name__, url_prefix='/profiles')


@bp.route('/', methods=['GET'])
def home():
    users = get_all_profiles()

    return render_template('home.html', index_table=users)


@bp.route('/hello', methods=['GET'])
def profiles():
    return render_template('home.html')