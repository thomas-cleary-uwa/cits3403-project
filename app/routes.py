""" define the routes for the flask application """


from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app import app
from app.forms import LoginForm, RegistrationForm

from app.route_helpers import (
    route_helpers,
    login_helpers, register_helpers, logout_helpers,
    user_helpers, quiz_questions_helpers, result_helpers,
    user_stats_helpers, user_attempts_helpers,
    before_request_helpers
)


###############################################################################
# Routes for all users (login not required)
###############################################################################

@app.route('/')
@app.route('/index')
def index():
    """ index page route """
    if current_user.is_authenticated and current_user.is_admin:
        return render_template('admin_pages/admin_index.html', title="Admin")

    return render_template('user_pages/index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ user login route """
    # if user already logged in send them to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        return login_helpers.attempt_login(login_form)

    return render_template('login.html', title='Sign In', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ user registration route """
    # if a user is already logged in send them to the index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        return register_helpers.attempt_registration(register_form)

    return render_template('register.html', title='Register', form=register_form)


@app.route('/logout')
@login_required
def logout():
    """ user logout route """
    # log the current user out and redirect to the index page
    return logout_helpers.attempt_logout()

@app.route('/content') 
def content():
    return render_template('user_pages/content.html', title='Learn')


###############################################################################
# Routes for users that are logged in (excluding admin users)
###############################################################################

@app.route('/user_profile/<username>')
@login_required
def user(username):
    """ user profile route """

    has_access, returned_obj = user_helpers.attempt_load_user_profile(username)

    if not has_access:
        # redirect object returned
        return returned_obj

    # else user data tuple returned
    this_user, user_data = returned_obj
    attempts, this_users_stats = user_data

    return render_template(
        'user_pages/user_profile.html',
        user=this_user,
        user_stats=this_users_stats,
        attempts=attempts,
        title="{}'s Profile".format(username)
    )


@app.route('/quiz')
@login_required
def quiz():
    """ quiz start/resume route """
    route_helpers.update_random_seed()

    return render_template('user_pages/quizLanding.html', title="Quiz")


@app.route('/quiz_questions/', methods=['GET','POST'])
@login_required
def quiz_questions():
    """ quiz questions/form route """

    redirected, return_obj = quiz_questions_helpers.create_quiz()
    if redirected:
        # returned a redirect object
        return return_obj

    return render_template('user_pages/quizQuestions.html',form=return_obj, title="Quiz")


@app.route('/result/<score>/<attempt_id>')
@login_required
# remove score and get from attempt row with the id
def result(score, attempt_id):
    """ quiz results page route """
    # in case we are coming from profile->results->quiz and seed has not yet been set
    route_helpers.update_random_seed()

    attempt_data, num_questions = result_helpers.get_result_data(attempt_id)

    return render_template(
        'user_pages/result.html',
        outcome=score,
        attempt=attempt_data,
        num_questions=num_questions,
        title="Results"
    )


###############################################################################
# Routes for Admin Users
###############################################################################

@app.route('/user_stats')
@login_required
def user_stats():
    """ route for admin to view users statistics """
    redirected, redirect_obj = route_helpers.check_admin_access()
    if redirected:
        return redirect_obj

    users, all_users_stats, totals = user_stats_helpers.get_user_stat_data()

    return render_template(
        'admin_pages/user_stats.html',
        user_info=zip(users, all_users_stats),
        totals=totals,
        title="User Stats"
    )


@app.route('/user_attempts/<username>')
@login_required
def user_attempts(username):
    """ route for admin to view users attempts """
    redirected, redirect_obj = route_helpers.check_admin_access()
    if redirected:
        return redirect_obj

    if username == "all":
        attempt_landing_data = user_attempts_helpers.get_landing_data()

        return render_template(
            'admin_pages/user_attempts_landing.html', 
            users=attempt_landing_data,
            title="User's Attempts"
        )

    users_attempts, attempt_keys = user_attempts_helpers.get_users_attempts(username)

    return render_template(
        'admin_pages/user_attempts.html',
        user_attempts=users_attempts,
        username=username,
        attempt_keys=attempt_keys,
        title="{}'s Attempts".format(username)
    )


###############################################################################
# Functions to call before a request is made
###############################################################################

@app.before_request
def before_request():
    """ things to do before handling requests """
    before_request_helpers.do_before_request()
