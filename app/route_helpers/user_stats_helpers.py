""" helper functions for user_stats route """

from app.models import UserStats
from app.route_helpers.route_helpers import get_all_users


def get_user_stat_data():
    """ return tuple of (users, individual_user_stats, all_user_stats) """
    users = get_all_users()

    user_stats = []
    for user in users:
        user_stats.append(UserStats.query.filter_by(user_id=user.id).first())

    totals = {}
    attempt_exists = False

    for stats in user_stats:
        totals["login_attempts"] = totals.get("login_attempts", 0) + stats.num_logins

        if stats.average_score is not None:
            attempt_exists = True

            totals["average"] = round(
                (
                (totals.get("average", 0) * totals.get("num_averages_added", 0)) +
                 stats.average_score
                ) /
                (totals.get("averages_added", 0) + 1),
                2 # round to 2 places
            )

    if not attempt_exists:
        totals["average"] = None

    return (users, user_stats, totals)