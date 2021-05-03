""" initialise the flask application """

from flask import Flask

from flask_admin import Admin
from flask_admin.menu import MenuLink

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_login import LoginManager, current_user

from config import Config


# represents the Flask application
app = Flask(__name__)

# set Flask configuration to be that defined in config.py
app.config.from_object(Config)

# represents the applications database
db = SQLAlchemy(app)

# represents the applications database migration engine
migrate = Migrate(app, db)

# represents the applications login manager
login = LoginManager(app)
# flask-login needs to know the view/route that handles login
login.login_view = 'login'


# import these here to avoid circular import errors
from app import routes, models, admin_views


# represents the admin interface manager
admin = Admin(app, name="Admin Tools", index_view=admin_views.MyAdminIndexView())

# adds database tables to the admin interface
admin.add_view(admin_views.AdminUserView(models.User, db.session))
admin.add_view(admin_views.AdminModelView(models.Question, db.session))
admin.add_view(admin_views.AdminAttemptView(models.SubmittedAttempt, db.session))
admin.add_view(admin_views.AdminAttemptView(models.SavedAttempt, db.session))

# adds link in admin interface to go back to the main site
admin.add_link(MenuLink(name="Back to Site", url="/index", category="Links"))