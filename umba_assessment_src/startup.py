from flask import (
    Blueprint
)

from umba_assesment_src.db import init_db

bp = Blueprint('startup', __name__, url_prefix='/initialize')


@bp.route('/')
def home():
    init_db()
    return "Application DB Populate"
