""" helper functions for the quiz_questions route in routes """

import random

from datetime import datetime

from flask import session
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

from app import db
from app.models import User, Question, SubmittedAttempt, SavedAttempt, UserStats
from .constants import NUM_QUESTIONS_IN_QUIZ


def get_user_stats():
    """ return tuple of (combined_user_stats, individual_user_stats) """
    users = User.query.filter(User.username != "admin").all()

    user_stats = []
    for user in users:
        user_stats.append(UserStats.query.filter_by(user_id=user.id).first())

    return (users, user_stats)


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


def delete_saved_attempts():
    """ delete all the saved attempts the current user has in the database """
    saved_attempts = SavedAttempt.query.filter_by(
        user_id=current_user.id).all()

    for attempt in saved_attempts:
        db.session.delete(attempt)

    current_user.has_saved_attempt = False

    db.session.commit()


def get_saved_attempt():
    """ gets the saved attempt the current user has in the database.
        returns a list of the questions and the responses previously entered by
        the user
    """
    saved_attempt = SavedAttempt.query.filter_by(
        user_id=current_user.id).first()

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
    all_questions = Question.query.all()
    random.Random(session["quiz_seed"]).shuffle(all_questions)
    return all_questions[:num_questions]


def get_question_choices(question):
    """ get a list of the choices for the field constructor """
    choices = [
        (question.answer,  question.answer),
        (question.wrong_1, question.wrong_1),
        (question.wrong_2, question.wrong_2),
        (question.wrong_3, question.wrong_3)
    ]

    return choices


def create_quiz_form():
    """ returns a quiz form and a list of the questions in it """

    class QuizForm(FlaskForm):
        """ form for the quiz questions """
        # submit button
        submit = SubmitField('Submit Test')
        # save button
        save = SubmitField('Save Test')


    if current_user.has_saved_attempt:
        questions, defaults = get_saved_attempt()

    else:
        questions = get_questions(NUM_QUESTIONS_IN_QUIZ)
        defaults = [None] * len(questions)

    choice_seed_modifier = 1
    for question, default in zip(questions, defaults):
        question_choices = get_question_choices(question)
        # randomise the order of the choices so not just answer,wrong,wrong,wrong
        random.Random(session["quiz_seed"] +
                      choice_seed_modifier).shuffle(question_choices)
        # change the order for the next question
        choice_seed_modifier += 1

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

    # might return summary and use for results page?
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

    score = sum(marks)
    score = int((score / NUM_QUESTIONS_IN_QUIZ) * 100)

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

    attempt_id = SubmittedAttempt.query.filter_by(user_id=current_user.id).order_by(SubmittedAttempt.id.desc()).first().id

    # update seed so next attempt is differnt if press 'try again'
    try:
        session["quiz_seed"] += 1
    except KeyError:
        session["quiz_seed"] = random.randint(1, 100)

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
