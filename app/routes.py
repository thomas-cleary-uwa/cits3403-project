from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, QuizForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Question, SubmittedAttempt, SavedAttempt
from werkzeug.urls import url_parse
from datetime import datetime

NUM_QUESTIONS_IN_QUIZ = 3

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    attempts = SubmittedAttempt.query.filter_by(user_id=current_user.id)
    numAttempts = attempts.count()

    all_scores = []

    for attempt in attempts:
        i = attempt.score
        all_scores.append(i)

    total = sum(all_scores)
    print("Total: {}, numAttempts: {}".format(total, numAttempts))
    if numAttempts == 0:
        average = None
    else:
        average = total / (numAttempts * NUM_QUESTIONS_IN_QUIZ)
        average = int(average * 100)

    return render_template('user.html', user=user, attempts=attempts, average=average, numAttempts=numAttempts)


@app.route('/quiz')
@login_required
def quiz():
    return render_template('quizStartPage.html')


@app.route('/quizQuestions', methods=['GET','POST'])
@login_required
def quiz_questions():
    NUM_NON_QUESTION_FIELDS = 3 # 2 Submits and 1 hidden?

    form, questions = create_question_form()

    if form.validate_on_submit():

        if form.submit.data:

            score = submit_attempt(form, questions)

            if current_user.has_saved_attempt:
                delete_saved_attempts()

            return render_template('result.html',form=form, outcome=score)
        

    # save button was pressed
    if form.save.data:

        if current_user.has_saved_attempt:
            delete_saved_attempts()

        save_attempt(form, questions)

        return redirect(url_for('quiz'))

    else:
        print(form.errors)

    return render_template('quizQuestions.html',form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


""" 
-------------------------------------------------------------------------------
Below are helper functions for the route functions
-------------------------------------------------------------------------------
"""

def delete_saved_attempts():
        savedAttempts = SavedAttempt.query.filter_by(user_id=current_user.id).all()

        for attempt in savedAttempts:
            db.session.delete(attempt)

        current_user.has_saved_attempt = False

        db.session.commit()


def get_saved_attempt():
    saved_attempt = SavedAttempt.query.filter_by(user_id=current_user.id).first()

    questions = [
        Question.query.get(saved_attempt.question_a_id),
        Question.query.get(saved_attempt.question_b_id),
        Question.query.get(saved_attempt.question_c_id)
    ]

    saved_responses = [
        saved_attempt.response_a,
        saved_attempt.response_b,
        saved_attempt.response_c
    ]

    return(questions, saved_responses)


def get_radio_fields(form):
    fields = [field for field in form]
    fields = fields[:-NUM_QUESTIONS_IN_QUIZ]
    return fields


def get_questions(num_questions):
    questions = []
    for i in range(1, num_questions+1):
        question = Question.query.get(i)
        questions.append(question)

    return questions


def create_question_form():
    if current_user.has_saved_attempt:
        questions, saved_responses = get_saved_attempt()

        # create quiz form
        form = QuizForm(
            question1=saved_responses[0],   # set default values field.default doesn't work
            question2=saved_responses[1],
            question3=saved_responses[2]
        )
        
        # get radiofield fields from form
        fields = get_radio_fields(form)

        index = 0
        for field in fields:
            question      = questions[index]
            field.label   = question.question

            field.choices = [
                (1, question.response_a), 
                (2, question.response_b),
                (3, question.response_c)
            ]

            index += 1


    else:
        form = QuizForm()
    
        fields = get_radio_fields(form)

        questions = get_questions(len(fields))

        index = 0
        for field in fields:
            question = questions[index]
            field.label = question.question

            field.choices = [
                (1, question.response_a), 
                (2, question.response_b),
                (3, question.response_c)
            ]

            index += 1

    return (form, questions)


def submit_attempt(form, questions):
    if Question.query.get(1).answer == form.question1.data: value_a = 1
    else: value_a = 0
    if Question.query.get(2).answer == form.question2.data: value_b = 1
    else: value_b = 0
    if Question.query.get(3).answer == form.question3.data: value_c = 1
    else: value_c = 0

    score = value_a + value_b + value_c

    attempt = SubmittedAttempt( 
        user_id=current_user.id,

        # change this from being hard coded for question id
        question_a_id = questions[0].id,
        response_a=form.question1.data, 
        mark_a=value_a,

        question_b_id = questions[1].id,
        response_b=form.question2.data, 
        mark_b=value_b, 

        question_c_id = questions[2].id,
        response_c=form.question3.data, 
        mark_c=value_c,
            
        score = score,
        attempt_datetime = datetime.utcnow()
    )

    db.session.add(attempt)
    db.session.commit()

    return score


def save_attempt(form, questions):
    savedAttempt = SavedAttempt(
        user_id=current_user.id,

        # change this from being hard coded for question id
        question_a_id  = questions[0].id,
        response_a     = form.question1.data, 

        question_b_id  = questions[1].id,
        response_b     = form.question2.data, 

        question_c_id  = questions[2].id,
        response_c     = form.question3.data, 

        saved_datetime = datetime.utcnow()
    )

    db.session.add(savedAttempt)
    current_user.has_saved_attempt = True
    db.session.commit()