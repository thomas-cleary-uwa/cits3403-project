""" helper functions for the result route """

from app.models import SubmittedAttempt, Question
from app.constants import NUM_QUESTIONS_IN_QUIZ


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


def get_result_data(attempt_id):
    """ returns data needed to render result page """
    return (
        get_attempt_data(SubmittedAttempt.query.get(attempt_id)),
        NUM_QUESTIONS_IN_QUIZ
    )
