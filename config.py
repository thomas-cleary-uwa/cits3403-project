import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password123'
    SQLALCHEMY_DATABASE_URI = 'postgres://lpsfasifwrqwjl:d4ed880cb09f0eb42c74601dc06491ef4eef1dda21207d307d0b4c65820cf01d@ec2-34-200-94-86.compute-1.amazonaws.com:5432/dche9bn7cuk1m8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # FLASK_ADMIN_SWATCH = "slate"