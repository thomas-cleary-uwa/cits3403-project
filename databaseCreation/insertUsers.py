import os, sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentDir)
sys.path.insert(0, parentdir)

from app import db
from app.models import User, Quiz


def addDummyUsers():
    """ adds users to the database for testing purposes """

    thomas = User(username="thomas", email="thomas@email.com")
    thomas.set_password("admin")
    db.session.add(thomas)

    michael = User(username="michael", email="michael@email.com")
    michael.set_password("admin")
    db.session.add(michael)

    calvin = User(username="calvin", email="calvin@email.com")
    calvin.set_password("admin")
    db.session.add(calvin)

    jason = User(username="jason", email="jason@email.com")
    jason.set_password("admin")
    db.session.add(jason)

    db.session.commit()




def main():
    addDummyUsers()


if __name__ == "__main__":
    main()
