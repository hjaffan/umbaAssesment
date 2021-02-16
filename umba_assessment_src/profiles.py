from flask import (
    Blueprint, render_template
)


from umba_assesment_src.db import get_all_profiles

bp = Blueprint('profiles', __name__, url_prefix='/profiles')

# TODO: Implement a JSON response call with pagination
@bp.route('/', methods=['GET'])
def home():
    users = get_all_profiles()

    return render_template('home.html', index_table=users)
