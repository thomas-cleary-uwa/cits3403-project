""" define the routes for the flask application """

import random

from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, SubmittedAttempt, UserStats

from app.route_helpers.old_route_helpers import * 
from app.route_helpers.route_helpers import *
from app.route_helpers.login_helpers import attempt_login
from app.route_helpers.logout_helpers import attempt_logout
from app.route_helpers.register_helpers import attempt_registration
from app.route_helpers.user_helpers import attempt_load_user_profile
from app.route_helpers.quiz_questions_helpers import create_quiz
from app.route_helpers.result_helpers import get_result_data

from app.constants import NUM_QUESTIONS_IN_QUIZ


###############################################################################
# Routes for all users (login not required)
###############################################################################

@app.route('/')
@app.route('/index')
def index():
    """ index page route """
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ user login route """
    # if user already logged in send them to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        return attempt_login(login_form)

    return render_template('login.html', title='Sign In', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ user registration route """
    # if a user is already logged in send them to the index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        return attempt_registration(register_form)

    return render_template('register.html', title='Register', form=register_form)


@app.route('/logout')
@login_required
def logout():
    """ user logout route """
    # log the current user out and redirect to the index page
    return attempt_logout()


###############################################################################
# Routes for users that are logged in (excluding admin users)
###############################################################################

@app.route('/user_profile/<username>')
@login_required
def user(username):
    """ user profile route """

    has_access, returned_obj = attempt_load_user_profile(username)

    if not has_access:
        # redirect object returned
        return returned_obj

    # else user data tuple returned
    user, user_data = returned_obj
    attempts, user_stats = user_data

    return render_template(
        'user_profile.html',
        user=user, 
        user_stats=user_stats, 
        attempts=attempts
    )


@app.route('/quiz')
@login_required
def quiz():
    """ quiz start/resume route """
    update_random_seed()
    return render_template('quizLanding.html')


@app.route('/quiz_questions/', methods=['GET','POST'])
@login_required
def quiz_questions():
    """ quiz questions/form route """

    redirected, return_obj = create_quiz()
    if redirected:
        # returned a redirect object
        return return_obj

    return render_template('quizQuestions.html',form=return_obj)


@app.route('/result/<score><attempt_id>')
@login_required
def result(score, attempt_id):
    """ quiz results page route """
    attempt_data, num_questions = get_result_data(attempt_id)

    return render_template(
        'result.html',
        outcome=score,
        attempt=attempt_data,
        num_questions=num_questions
    )


###############################################################################
# Routes for Admin Users
###############################################################################

@app.route('/user_stats')
@login_required
def user_stats():
    """ route for admin to view users statistics """
    if not current_user.is_admin:
        flash('Access Denied')
        return redirect(url_for('index'))

    users, user_stats, totals = get_user_stats()

    return render_template('user_stats.html', user_info=zip(users, user_stats), totals=totals)


@app.route('/user_attempts/<username>')
@login_required
def user_attempts(username):

    """ route for admin to view users attempts """
    if not current_user.is_admin:
        flash('Access Denied')
        return redirect(url_for('index'))

    if username == "all":
        users = get_all_users()
        quiz_attempt_counts = []
        for user in users:
            quiz_attempt_counts.append(UserStats.query.filter_by(user_id=user.id).first().num_quiz_attempts)
        return render_template('user_attempts_landing.html', users=zip(users, quiz_attempt_counts))
    
    users_attempts = get_users_attempts(username)

    attempt_keys = []
    template = "question_"
    for i in range(1,NUM_QUESTIONS_IN_QUIZ+1):
        attempt_keys.append(template + str(i))

    return render_template('user_attempts.html',
     user_attempts=users_attempts, username=username, attempt_keys=attempt_keys
    )


###############################################################################
# Functions to call before a request is made
###############################################################################

@app.before_request
def before_request():
    """ things to do before handling requests """
    # update the time this user was last seen on the website
    if current_user.is_authenticated and not current_user.is_admin:
        UserStats.query.filter_by(user_id=current_user.id).first().last_seen = datetime.utcnow()
        db.session.commit()
