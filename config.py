import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite3:///' + os.path.join(basedir, 'app.bd')
    SQLALCHEMY_TRACK_MODIFICATIONS = False