# adds the app to the PATH variable
import os, sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentDir)
sys.path.insert(0, parentdir)

from app import db
from app.models import User


def addAdmin():
    """ adds admin user to database """

    admin = User(username="admin", email="admin@email.com", isAdmin=True)
    admin.set_password("admin")
    db.session.add(admin)

    db.session.commit()


def main():
    addAdmin()


if __name__ == "__main__":
    main()
