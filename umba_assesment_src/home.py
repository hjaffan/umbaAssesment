import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flask_paginate import Pagination, get_page_args

from umba_assesment_src.db import get_all_profiles

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total, users = get_all_profiles(offset=offset, per_page=per_page)

    pagination = Pagination(page=page, total=total,  per_page=per_page, css_framework='bootstrap4')

    return render_template('homepage.html', index_table=users, pagination=pagination)
