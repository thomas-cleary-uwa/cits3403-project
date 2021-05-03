"""
Creates the SQLite database for the application.
Inserts an admin user for the website
Inserts 3 dummy quiz questions
"""

import os
import sys

# add app to Python PATH variable
currentDir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentDir)
sys.path.insert(0, parentdir)

from app import db
from app.models import User, Question


def add_admin():
    """ adds admin user to database """

    admin = User(username="admin", email="admin@email.com", is_admin=True)
    admin.set_password("admin")
    db.session.add(admin)
    db.session.commit()


def add_quiz():
    """ adds quiz questions to the database for testing purposes """

    q_1 = Question(question='1?', response_a='N', response_b='Y', response_c='N', answer=2)
    db.session.add(q_1)

    q_2 = Question(question='2?', response_a='N', response_b='N', response_c='Y', answer=3)
    db.session.add(q_2)

    q_3 = Question(question='3?', response_a='Y', response_b='N', response_c='N', answer=1)
    db.session.add(q_3)

    db.session.commit()


def print_start_message(message=None):
    """ print starting message for function call """
    print("-" * 80)
    print(message)
    print()


def print_finished_message(message=None):
    """ print finished message for function call """
    print()
    print(message)
    print("-" * 80)
    print()


def create_database():
    """ creates database for the website """
    print_start_message("Initialising Database [ flask db init ]")
    os.system("flask db init")
    print_finished_message("Database initialised")

    print_start_message("Creating database migration script [ flask db migrate ]")
    os.system("flask db migrate")
    print_finished_message("Database migrated")

    print_start_message("Upgrading database [ flask db upgrade ]")
    os.system("flask db upgrade")
    print_finished_message("Database upgraded")

    print_start_message("Inserting admin user into database" + \
    """
    admin = User(username="admin", email="admin@email.com", isAdmin=True)
    admin.set_password("admin")
    db.session.add(admin)
    db.session.commit()"
    """
    )
    add_admin()
    print_finished_message("admin inserted [Username='admin', Password='admin']")

    print_start_message("Inserting quiz questions into database" + \
    """
    q1 = Quiz(question='1?', response_a='N', response_b='Y', response_c='N', answer=2)
    db.session.add(q1)

    q2 = Quiz(question='2?', response_a='N', response_b='N', response_c='Y', answer=3)
    db.session.add(q2)

    q3 = Quiz(question='3?', response_a='Y', response_b='N', response_c='N', answer=1)
    db.session.add(q3)

    db.session.commit()
    """
    )
    add_quiz()
    print_finished_message("quiz inserted")

def main():
    """ only run this file when you don't have a migrations folder and app.db """
    create_database()


if __name__ == "__main__":
    main()
