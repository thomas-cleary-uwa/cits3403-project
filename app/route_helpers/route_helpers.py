""" general helper functions for all routes in routes.py """

import random

from flask import flash, request, url_for, session
from flask_login import current_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app.models import User, Question
from app.constants import NUM_QUESTIONS_IN_QUIZ


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


def check_admin_access():
    """ returns (false, none) is user is admin else (false, redirect) """
    redirected = False

    if not current_user.is_admin:
        flash('Access Denied')
        redirected = True
        return (redirected, redirect(url_for('index')))
    
    return (redirected, None)


def get_attempt_data(attempt):
    """ returns list of informative data about a submitted attempt
        for the results page
    """
    key_template = "question_"

    question_ids = [
        attempt.question_1_id,
        attempt.question_2_id,
        attempt.question_3_id,
        attempt.question_4_id,
        attempt.question_5_id,
    ]

    responses = [
        attempt.response_1,
        attempt.response_2,
        attempt.response_3,
        attempt.response_4,
        attempt.response_5,
    ]

    marks = [
        attempt.mark_1,
        attempt.mark_2,
        attempt.mark_3,
        attempt.mark_4,
        attempt.mark_5,
    ]

    attempt_data = {}

    for i in range(1, NUM_QUESTIONS_IN_QUIZ+1):
        key = key_template + str(i)

        attempt_data[key] = {
            "question" : Question.query.get(question_ids[i-1]).question,
            "response" : responses[i-1],
            "mark"     : marks[i-1]
        }

    return attempt_data