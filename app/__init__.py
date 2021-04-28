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


from app import routes, models


admin = Admin(app, name="INSERT NAME HERE", template_mode="bootstrap3")

admin.add_view(models.AdminModelView(models.User, db.session))
admin.add_link(MenuLink(name="Back to Site", url="/index", category="Links"))