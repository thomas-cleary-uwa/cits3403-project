""" helper functions for the quiz_questions route """

import random

from flask import session, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

from app.route_helpers.route_helpers import update_random_seed

from app import db
from app.models import UserStats, Question, SavedAttempt, SubmittedAttempt
from app.constants import NUM_QUESTIONS_IN_QUIZ


def get_questions():
    """ returns a list of questions from the database of length, num_questions """
    all_questions = Question.query.all()
    random.Random(session["quiz_seed"]).shuffle(all_questions)

    questions = all_questions[:NUM_QUESTIONS_IN_QUIZ]
    choices = [None] * len(questions)

    return (questions, choices)


def get_question_choices(question):
    """ get a list of the choices for the field constructor """
    choices = [
        (question.answer,  question.answer),
        (question.wrong_1, question.wrong_1),
        (question.wrong_2, question.wrong_2),
        (question.wrong_3, question.wrong_3)
    ]

    return choices


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


def create_quiz_form():
    """ returns a quiz form and a list of the questions in it """

    class QuizForm(FlaskForm):
        """ form for the quiz questions """
        # submit button
        submit = SubmitField('Submit Test')
        # save button
        save = SubmitField('Save Test')


    if current_user.has_saved_attempt:
        questions, choices = get_saved_attempt()

    else:
        questions, choices = get_questions()

    seed = random.randint(1, 100)
    for question, choice in zip(questions, choices):
        question_choices = get_question_choices(question)

        # randomise the order of the choices so not just answer,wrong,wrong,wrong
        random.Random(seed).shuffle(question_choices)
        # change the order for the next question
        seed += 1

        question_field = RadioField(
            label=question.question,
            validators=[DataRequired()],
            choices=question_choices,
            default=choice
        )
        setattr(QuizForm, question.question, question_field)

        form = QuizForm()

    return (form, questions)


def get_most_recent_attempt_id():
    """ return id of most recent attempt for current user """
    return SubmittedAttempt.query.filter_by(user_id=current_user.id).order_by(SubmittedAttempt.id.desc()).first().id


def get_attempt_summary(form_data, questions, marks):
    """ create a dictionary summary of an attempt """
    summary = {}
    for i, curr_question in enumerate(questions):
        key = "question_" + str(i+1)

        summary[key] = {
            "question_id": curr_question.id,
            "question": curr_question.question,
            "response": form_data[curr_question.question],
            "mark": marks[i]
        }
        i += 1

    return summary


def submit_attempt(form, questions):
    """ mark the completed quiz attempt and save it to the database
        returns the score the user achieved and the attempts id
    """

    marks = []
    form_data = form.data

    marks = [1 if question.answer == form_data[question.question] else 0 for question in questions]

    # might return summary and use for results page?
    summary = get_attempt_summary(form_data, questions, marks)

    score = int((sum(marks) / NUM_QUESTIONS_IN_QUIZ) * 100)

    attempt = SubmittedAttempt(
        user_id=current_user.id,

        question_1_id=summary["question_1"]["question_id"],
        response_1=summary["question_1"]["response"],
        mark_1=summary["question_1"]["mark"],

        question_2_id=summary["question_2"]["question_id"],
        response_2=summary["question_2"]["response"],
        mark_2=summary["question_2"]["mark"],

        question_3_id=summary["question_3"]["question_id"],
        response_3=summary["question_3"]["response"],
        mark_3=summary["question_3"]["mark"],

        question_4_id=summary["question_4"]["question_id"],
        response_4=summary["question_4"]["response"],
        mark_4=summary["question_4"]["mark"],

        question_5_id=summary["question_5"]["question_id"],
        response_5=summary["question_5"]["response"],
        mark_5=summary["question_5"]["mark"],

        score=score
    )

    db.session.add(attempt)
    db.session.commit()

    attempt_id = get_most_recent_attempt_id()

    # update seed so next attempt is differnt if press 'try again'
    update_random_seed()

    return (score, attempt_id)



def save_attempt(form, questions):
    """ save the partially completed quiz attempt to the database """
    form_data = form.data

    saved_attempt = SavedAttempt(
        user_id=current_user.id,

        question_1_id=questions[0].id,
        response_1=form_data[questions[0].question],

        question_2_id=questions[1].id,
        response_2=form_data[questions[1].question],

        question_3_id=questions[2].id,
        response_3=form_data[questions[2].question],

        question_4_id=questions[3].id,
        response_4=form_data[questions[3].question],

        question_5_id=questions[4].id,
        response_5=form_data[questions[4].question],

        saved_datetime=datetime.utcnow()
    )

    db.session.add(saved_attempt)
    current_user.has_saved_attempt = True
    db.session.commit()


def create_quiz():
    """ returns the quiz form to render in quizQuestions.html """

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

            # update user stats for num attempts MOVE THIS TO EXTERNAL FUNCTION
            user_stats = UserStats.query.filter_by(user_id=current_user.id).first()
            if user_stats.highest_score is None:
                user_stats.highest_score = score
            elif user_stats.highest_score < score:
                user_stats.highest_score = score

            user_average = user_stats.average_score

            if user_average is None:
                user_stats.average_score = score
            
            else:
                old_average_total = user_average * user_stats.num_quiz_attempts

            user_stats.num_quiz_attempts += 1

            if user_average is not None:
                new_average = (old_average_total + score) / user_stats.num_quiz_attempts
                user_stats.average_score = round(new_average, 2)

            db.session.commit()

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

    return form

