""" helper functions for the quiz route """

import random
from flask import session


def update_random_seed():
    """ update/set the random seed for quiz question generation """
    try:
        session["quiz_seed"] += 1
    except KeyError:
        session["quiz_seed"] = random.randint(1, 100)
