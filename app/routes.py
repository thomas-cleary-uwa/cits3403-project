""" define the routes for the flask application """

import random

from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, SubmittedAttempt
from .route_helpers import create_quiz_form, submit_attempt, delete_saved_attempts
from .route_helpers import save_attempt, get_attempt_data
from .constants import NUM_QUESTIONS_IN_QUIZ


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

    form = LoginForm()

    # if form data is valid when submitted
    if form.validate_on_submit():

        # try and find the user with the entered username
        user = User.query.filter_by(username=form.username.data).first()

        # if we couldn't find a user with the entered username or the password
        # is invalid, flash an error message on the page
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))

        # if username and password are correct log in the user
        login_user(user, remember=form.remember_me.data)

        # if user was redirected to the login page, send them back to where
        # they came from, else send them to the index page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    """ user logout route """
    # log the current user out and redirect to the index page
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    """ user registration route """
    # if a user is already logged in send them to the index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    # if form is submitted with valid data
    if form.validate_on_submit():
        # create the new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # add the user to the database
        db.session.add(user)
        db.session.commit()

        # flash a message to the screen for the user
        flash("Congratulations, you are now a registered user!")

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)



@app.route('/user_profile/<username>')
@login_required
def user(username):
    """ user profile route """

    # if user trys to view another persons profile, redirect them to their own
    if username != current_user.username:
        flash('You can not access other user\'s profiles')
        return redirect(url_for('user', username=current_user.username))

    if current_user.is_admin:
        flash('Administrators do not have a profile')
        return redirect(url_for('index'))

    user = User.query.filter_by(username=username).first_or_404()

    # retrieve all the quiz attempts for this user
    attempts = SubmittedAttempt.query.filter_by(user_id=current_user.id)

    # list of the scores for each attempt
    all_scores = [attempt.score for attempt in attempts]

    total = sum(all_scores)
    num_attempts = len(all_scores)

    # calculate average score
    if num_attempts == 0:
        average = None
    else:
        average = total / num_attempts
        average = round(average, 2)

    return render_template(
        'user_profile.html', user=user, attempts=attempts,
        average=average, num_attempts=num_attempts
    )



@app.route('/quiz')
@login_required
def quiz():
    """ quiz start/resume route """
    try:
        session["quiz_seed"] += 1
    except KeyError:
        session["quiz_seed"] = random.randint(1, 100)

    return render_template('quizLanding.html')



@app.route('/quiz_questions/', methods=['GET','POST'])
@login_required
def quiz_questions():
    """ quiz questions/form route """

    # get the quiz Form and the list of questions that will be in the quiz
    form, questions = create_quiz_form()

    # if the user has chosen an answer for each question
    if form.validate_on_submit():

        # if the submit button was pressed
        if form.submit.data:
            # calculate their score for this quiz
            score, attempt_id = submit_attempt(form, questions)
            # if they had this quiz saved before, delete it from the database
            if current_user.has_saved_attempt:
                delete_saved_attempts()

            return redirect(url_for('result', score=score, attempt_id=attempt_id))


    # if the save button was pressed
    if form.save.data:
        # delete any previously saved attempt
        if current_user.has_saved_attempt:
            delete_saved_attempts()
        # save this attempt
        save_attempt(form, questions)

        return redirect(url_for('quiz'))

    # print errors if submit was pressed but not all questions answered
    else:
        print(form.errors)

    return render_template('quizQuestions.html',form=form)


@app.route('/result/<score><attempt_id>')
@login_required
def result(score, attempt_id):
    """ quiz results page route """
    attempt = SubmittedAttempt.query.get(attempt_id)
    attempt_data = get_attempt_data(attempt)
    return render_template(
        'result.html',
        outcome=score,
        attempt=attempt_data,
        num_questions=NUM_QUESTIONS_IN_QUIZ
    )


@app.route('/user_stats')
@login_required
def user_stats():
    """ route for admin to view users statistics """
    if not current_user.is_admin:
        flash('Access Denied')
        return redirect(url_for('index'))

    return render_template('user_stats.html')


@app.before_request
def before_request():
    """ things to do before handling requests """
    # update the time this user was last seen on the website
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
