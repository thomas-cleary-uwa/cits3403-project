""" 

Sets up the database for the flask application
Inserts an admin user with username: 'admin' password: 'admin'

"""

import os
import sys
import csv

# add app to Python PATH variable
currentDir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentDir)
sys.path.insert(0, parentdir)

from app import db
from app.models import User, Question, UserStats



def add_admin():
    """ adds admin user to database """

    admin = User(username="admin", email="admin@email.com", is_admin=True)
    admin.set_password("admin")
    db.session.add(admin)
    db.session.commit()


def get_quiz_questions():
    """ get quiz questions from INFILE """

    INFILE = "./setup/quiz_questions.csv"

    questions = []

    with open(INFILE, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        reader = list(reader)

        for row in reader[1:]:
            questions.append(row)

    return questions


def add_quiz():
    """ adds quiz questions to the database for testing purposes """
    
    questions = get_quiz_questions()

    for question in questions:
        new_question = Question(
            question = question[0],
            answer   = question[1],
            wrong_1  = question[2],
            wrong_2  = question[3],
            wrong_3  = question[4],
        )
        db.session.add(new_question)
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

    print_start_message("Inserting quiz questions into database")
    add_quiz()
    print_finished_message("quiz inserted")


def main():
    """ only run this file when you don't have a migrations folder and app.db """
    create_database()


if __name__ == "__main__":
    main()
