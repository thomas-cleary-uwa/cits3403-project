""" define the routes for the flask application """

import random

from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from wtforms import RadioField
from wtforms.validators import DataRequired

from app import app, db
from app.forms import LoginForm, RegistrationForm, QuizForm
from app.models import User, Question, SubmittedAttempt, SavedAttempt



# Constants
NUM_QUESTIONS_IN_QUIZ = 5



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

    user = User.query.filter_by(username=username).first_or_404()

    # retrieve all the quiz attempts for this user
    attempts = SubmittedAttempt.query.filter_by(user_id=current_user.id)
    num_attempts = attempts.count()

    # list of the scores for each attempt
    all_scores = [attempt.score for attempt in attempts]

    total = sum(all_scores)

    # calculate average score
    if num_attempts == 0:
        average = None
    else:
        average = total / (num_attempts * NUM_QUESTIONS_IN_QUIZ)
        average = int(average * 100)

    return render_template(
        'user.html', user=user, attempts=attempts,
        average=average, numAttempts=num_attempts
    )



@app.route('/quiz')
@login_required
def quiz():
    """ quiz start/resume route """
    return render_template('quizLanding.html')



@app.route('/quiz_questions', methods=['GET','POST'])
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
            score = submit_attempt(form, questions)

            # if they had this quiz saved before, delete it from the database
            if current_user.has_saved_attempt:
                delete_saved_attempts()

            return render_template(
                'result.html',
                form=form, 
                outcome=score, 
                num_questions=NUM_QUESTIONS_IN_QUIZ
            )


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



@app.before_request
def before_request():
    """ things to do before handling requests """
    # update the time this user was last seen on the website
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



###############################################################################
# Below are helper functions for the route functions
###############################################################################

def delete_saved_attempts():
    """ delete all the saved attempts the current user has in the database """
    saved_attempts = SavedAttempt.query.filter_by(user_id=current_user.id).all()

    for attempt in saved_attempts:
        db.session.delete(attempt)

    current_user.has_saved_attempt = False

    db.session.commit()



def get_saved_attempt():
    """ gets the saved attempt the current user has in the database.
        returns a list of the questions and the responses previously entered by
        the user
    """
    saved_attempt = SavedAttempt.query.filter_by(user_id=current_user.id).first()

    questions = [
        Question.query.get(saved_attempt.question_1_id),
        Question.query.get(saved_attempt.question_2_id),
        Question.query.get(saved_attempt.question_3_id),
        Question.query.get(saved_attempt.question_4_id),
        Question.query.get(saved_attempt.question_5_id)
    ]

    saved_responses = [
        saved_attempt.response_1,
        saved_attempt.response_2,
        saved_attempt.response_3,
        saved_attempt.response_4,
        saved_attempt.response_5
    ]

    return(questions, saved_responses)



def get_questions(num_questions):
    """ returns a list of questions from the database of length, num_questions """
    questions = []
    for i in range(1, num_questions+1):
        question = Question.query.get(i)
        questions.append(question)

    return questions



def get_question_choices(question):
    """ get a list of the choices for the field constructor """
    choices = [
        (question.answer, question.answer),
        (question.wrong_1, question.wrong_1),
        (question.wrong_2, question.wrong_2),
        (question.wrong_3, question.wrong_3)
    ]

    return choices



def create_quiz_form():
    """ returns a quiz form and a list of the questions in it """
    if current_user.has_saved_attempt:
        questions, defaults = get_saved_attempt()

    else:
        questions = get_questions(NUM_QUESTIONS_IN_QUIZ)
        defaults = [None] * len(questions)

    for question, default in zip(questions, defaults):
        question_choices = get_question_choices(question)
        random.shuffle(question_choices)

        field = RadioField(
            label=question.question,
            validators=[DataRequired()],
            choices=question_choices,
            default=default
        )
        setattr(QuizForm, question.question, field)

        form = QuizForm()

    return (form, questions)



def submit_attempt(form, questions):
    """ mark the completed quiz attempt and save it to the database
        returns the score the user achieved
    """

    marks = []
    form_data = form.data

    for question in questions:
        if question.answer == form_data[question.question]:
            marks.append(1)
        else:
            marks.append(0)


    score = sum(marks)

    attempt = SubmittedAttempt(
        user_id=current_user.id,

        question_1_id = questions[0].id,
        response_1= form_data[questions[0].question],
        mark_1= marks[0],

        question_2_id = questions[1].id,
        response_2=form_data[questions[1].question],
        mark_2= marks[1],

        question_3_id = questions[2].id,
        response_3=form_data[questions[2].question],
        mark_3= marks[2],

        question_4_id = questions[3].id,
        response_4=form_data[questions[3].question],
        mark_4 = marks[3],

        question_5_id = questions[4].id,
        response_5=form_data[questions[4].question],
        mark_5 = marks[4],

        score = score,
        attempt_datetime = datetime.utcnow()
    )

    db.session.add(attempt)
    db.session.commit()

    return score



def save_attempt(form, questions):
    """ save the partially completed quiz attempt to the database """
    form_data = form.data

    saved_attempt = SavedAttempt(
        user_id        =current_user.id,

        question_1_id  = questions[0].id,
        response_1     = form_data[questions[0].question],

        question_2_id  = questions[1].id,
        response_2     = form_data[questions[1].question],

        question_3_id  = questions[2].id,
        response_3     = form_data[questions[2].question],

        question_4_id  = questions[3].id,
        response_4     = form_data[questions[3].question],

        question_5_id  = questions[4].id,
        response_5     = form_data[questions[4].question],

        saved_datetime = datetime.utcnow()
    )

    db.session.add(saved_attempt)
    current_user.has_saved_attempt = True
    db.session.commit()
