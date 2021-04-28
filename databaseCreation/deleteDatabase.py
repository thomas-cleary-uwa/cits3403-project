import os


def deleteDatabase():
    DATABASE_PATH = "./app.db"
    MIGRATIONS_PATH = "./migrations"

    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print()
        print("_" * 80)
        print("app.db removed")
        print("-" * 80)
        print()
    else:
        print()
        print("*" * 80)
        print("app.db does not exist")
        print("*" * 80)
        print()


    if os.path.exists(MIGRATIONS_PATH):
        for dirpath, dirnames, filenames in os.walk(MIGRATIONS_PATH):
            for filename in filenames:
                os.remove(dirpath + "/" + filename)
            if dirpath != MIGRATIONS_PATH:
                print(dirpath)
                os.rmdir(dirpath)
        os.rmdir(MIGRATIONS_PATH)
        print()
        print("-" * 80)
        print("migrations directory removed")
        print("-" * 80)
        print()
    else:
        print()
        print("*" * 80)
        print("app.db does not exist")
        print("*" * 80)
        print()
    
    
def main():
    """ delete all the database files """
    deleteDatabase()


if __name__ == "__main__":
    main()