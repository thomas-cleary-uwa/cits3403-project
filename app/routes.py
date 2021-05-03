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

    jobs = [
        {
            'person' : {'name' : 'Thomas'},
            'task' : 'login'
        },
        {
            'person' : {'name' : 'Calvin'},
            'task' : 'content'
        },
        {
            'person' : {'name' : 'Jason'},
            'task' : 'home page'
        },
        {
            'person' : {'name' : 'Michael'},
            'task' : 'quiz'
        }
    ]

    return render_template('index.html', jobs=jobs)


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

    if current_user.has_saved_attempt:
        saved_attempt = SavedAttempt.query.filter_by(user_id=current_user.id).first()
        if saved_attempt is None:
            # do some actual error checking
            print("error no saved attempt")

        else:
            # do something not hard coded once this is working
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

            # set default values field.default doesn't work
            form = QuizForm(
                question1=saved_responses[0],
                question2=saved_responses[1],
                question3=saved_responses[2]
            )
            
            fields = [field for field in form]
            fields = fields[:-NUM_QUESTIONS_IN_QUIZ]
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


    else:
    # REMOVE THIS LOGIC INTO SEPERATE FUNCTION
    # TO RANDOMISE THIS 
    # GET NUMBER OF ROWS IN QUESTION TABLE
    # SELECT RANDOM INT FROM 1->NUM_ROWS FOR NUMBER OF QUESTIONS ON QUIZ
    # SELECT THESE ROWS FROM THE TABLE TO BE THE QUIZ QUESTIONS
        # every field except the submit field
        form = QuizForm()
        questions = []
    
        fields = [field for field in form]
        fields = fields[:-NUM_QUESTIONS_IN_QUIZ]

        for i in range(1, len(fields)+1):
            question = Question.query.get(i)
            questions.append(question)

        index = 0
        for field in fields:
            question = questions[index]
            field.label = question.question
            # change to allow for as many questions as in the questions list
            field.choices = [
                (1, question.response_a), 
                (2, question.response_b),
                (3, question.response_c)
            ]

            index += 1

    print(form.csrf_token)

    if form.validate_on_submit():

        if form.submit.data:

            outcome = 0 # dummy value
            if Question.query.get(1).answer == form.question1.data: value_a = 1
            else: value_a = 0
            if Question.query.get(2).answer == form.question2.data: value_b = 1
            else: value_b = 0
            if Question.query.get(3).answer == form.question3.data: value_c = 1
            else: value_c = 0
            value_score = value_a + value_b + value_c

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
                    
                score = value_score,
                attempt_datetime = datetime.utcnow()
            )
            
            db.session.add(attempt)
            db.session.commit()

            # NEED TO DELETE ANY SAVED ATTEMPTS IN THE DATABASE FOR THIS USER 
            if current_user.has_saved_attempt:
                savedAttempts = SavedAttempt.query.filter_by(user_id=current_user.id).all()

                for attempt in savedAttempts:
                    db.session.delete(attempt)

                current_user.has_saved_attempt = False

                db.session.commit()

            outcome = value_score
            return render_template('result.html',form=form, outcome=outcome)
        

    # save button was pressed
    if form.save.data:

        # NEED TO DELETE ANY SAVED ATTEMPTS IN THE DATABASE FOR THIS USER 
        if current_user.has_saved_attempt:
            savedAttempts = SavedAttempt.query.filter_by(user_id=current_user.id).all()

            for attempt in savedAttempts:
                db.session.delete(attempt)

            current_user.has_saved_attempt = False

            db.session.commit()

        savedAttempt = SavedAttempt(
            user_id=current_user.id,
            
            # change this from being hard coded for question id
            question_a_id = questions[0].id,
            response_a=form.question1.data, 

            question_b_id = questions[1].id,
            response_b=form.question2.data, 

            question_c_id = questions[2].id,
            response_c=form.question3.data, 
                
            saved_datetime = datetime.utcnow()
        )

        db.session.add(savedAttempt)
        current_user.has_saved_attempt = True
        db.session.commit()


        return redirect(url_for('quiz'))

    else:
        print(form.errors)

    return render_template('quizQuestions.html',form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

