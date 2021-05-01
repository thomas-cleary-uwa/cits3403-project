# adds the app to the PATH variable
import os, sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentDir)
sys.path.insert(0, parentdir)

from app import db
from app.models import User
import os


def addAdmin():
    """ adds admin user to database """

    admin = User(username="admin", email="admin@email.com", isAdmin=True)
    admin.set_password("admin")
    db.session.add(admin)
    db.session.commit()


def createDatabase():
    """ creates database for your branch """
    print("-" * 80)
    print("Initialising Database [ flask db init ]")
    print()
    os.system("flask db init")
    print()
    print("Database initialised")
    print("-" * 80)
    print()

    print("-" * 80)
    print("Creating database migration script [ flask db migrate ]")
    print()
    os.system("flask db migrate")
    print()
    print("Database migrated")
    print("-" * 80)
    print()

    print("-" * 80)
    print("Upgrading database [ flask db upgrade ]")
    print()
    os.system("flask db upgrade")
    print()
    print("Database upgraded")
    print("-" * 80)
    print()

    print("-" * 80)
    print("Inserting admin user into database")
    print()
    print(
    """
    admin = User(username="admin", email="admin@email.com", isAdmin=True)
    admin.set_password("admin")
    db.session.add(admin)
    db.session.commit()" """
    )
    addAdmin() 
    print()
    print("admin inserted [Username='admin', Password='admin']")
    print("-" * 80)
    print()

def main():
    """ only run this file when you don't have a migrations folder and app.db """
    createDatabase()


if __name__ == "__main__":
    main()