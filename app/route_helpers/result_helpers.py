""" helper functions for the result route """

from app.route_helpers.route_helpers import get_attempt_data
from app.models import SubmittedAttempt, Question
from app.constants import NUM_QUESTIONS_IN_QUIZ 


def get_result_data(attempt_id):
    """ returns data needed to render result page """
    return (
        get_attempt_data(SubmittedAttempt.query.get(attempt_id)),
        NUM_QUESTIONS_IN_QUIZ
    )
