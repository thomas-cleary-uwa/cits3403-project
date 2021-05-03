""" Delete the database files for the app
    app.db
    ./migrations

    Run this file from the root directory ./cits3401-project
"""

import os


DATABASE_PATH = "./app.db"
MIGRATIONS_PATH = "./migrations"


def print_message(message):
    """ print a message to the terminal """
    print()
    print("-" * 80)
    print(message)
    print("-" * 80)


def delete_database():
    """ deletes app.db and ./migrations from root directory of flask app """

    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print_message("app.db removed")

    else:
        print_message("app.db does not exist")


    if os.path.exists(MIGRATIONS_PATH):
        for dirpath, _, filenames in os.walk(MIGRATIONS_PATH):
            for filename in filenames:
                os.remove(dirpath + "/" + filename)
            if dirpath != MIGRATIONS_PATH:
                print(dirpath)
                os.rmdir(dirpath)
        os.rmdir(MIGRATIONS_PATH)
        print_message("migrations directory removed")
    else:
        print_message("app.db does not exist")


def main():
    """ delete all the database files """
    delete_database()


if __name__ == "__main__":
    main()
