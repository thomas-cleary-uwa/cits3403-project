from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.menu import MenuLink


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


from app import routes, models, adminViews


admin = Admin(app, name="INSERT NAME HERE", template_mode="bootstrap3")

# adds these tables to admin page for editing
admin.add_view(adminViews.AdminUserView(models.User, db.session))
admin.add_view(adminViews.AdminModelView(models.Question, db.session))
admin.add_view(adminViews.AdminAttemptView(models.Attempt, db.session)) #  REMOVE CREATE TAB

# adds link to go back to website
admin.add_link(MenuLink(name="Back to Site", url="/index", category="Links"))