from flask import (
    Blueprint
)

from umba_assessment_src import db

bp = Blueprint('startup', __name__, url_prefix='/initialize')

@bp.route('/')
def home():
    db.init_db()
    return "Application DB Populate"
