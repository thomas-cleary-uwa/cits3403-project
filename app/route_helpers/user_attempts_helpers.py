""" helper functions for user_stats route """

from app.route_helpers.route_helpers import get_all_users, get_attempt_data

from app.models import UserStats, User, SubmittedAttempt
from app.constants import NUM_QUESTIONS_IN_QUIZ


def get_landing_data():
    """ return data for rendering landing page """
    users = get_all_users()

    quiz_attempt_counts = []
    for user in users:
        # get each users num_quiz_attempts
        quiz_attempt_counts.append(UserStats.query.filter_by(user_id=user.id).first().num_quiz_attempts)

    return zip(users, quiz_attempt_counts)


def get_users_attempts(username):
    """ return list of attempts for user with username"""

    user = User.query.filter_by(username=username).first()

    users_attempts = []

    attempts = SubmittedAttempt.query.filter_by(user_id=user.id).order_by(SubmittedAttempt.id).all()
    for attempt in attempts:
        users_attempts.append(get_attempt_data(attempt)) 

    attempt_keys = []
    template = "question_"
    for i in range(1,NUM_QUESTIONS_IN_QUIZ+1):
        attempt_keys.append(template + str(i))
    
    return (users_attempts, attempt_keys)