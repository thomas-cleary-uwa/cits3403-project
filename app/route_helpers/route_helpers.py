""" general helper functions for all routes in routes.py """

import random

from flask import request, url_for, session
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app.models import User


def get_user(username, four_zero_four=False):
    """ return the user with username=username """
    if four_zero_four:
        user = User.query.filter_by(username=username).first_or_404()
    else:
        user = User.query.filter_by(username=username).first()
    return user


def get_all_users():
    """ return a list of all user rows in db """
    return User.query.filter(User.username != "admin").all()


def redirect_next(default="index"):
    """ return redirect object with url for next otherwise default """
    next_page = request.args.get("next")

    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for(default)

    return redirect(next_page)


def update_random_seed():
    """ update/set the random seed for quiz question generation """
    try:
        session["quiz_seed"] += 1
    except KeyError:
        session["quiz_seed"] = random.randint(1, 100)
