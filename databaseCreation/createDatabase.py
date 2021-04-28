import os


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
    

def main():
    """ only run this file when you don't have a migrations folder and app.db """
    createDatabase()


if __name__ == "__main__":
    main()