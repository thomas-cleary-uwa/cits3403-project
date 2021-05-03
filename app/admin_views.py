""" customises each table view in the admin interface """

# flask
from flask import redirect, url_for

# flask-admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla import ModelView

# flask-login
from flask_login import current_user


class MyAdminIndexView(AdminIndexView):
    """ custome index view/route for the admin interface """

    def is_accessible(self):
        """ allow only admins to access the admin interface """
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        """ redirect to index page if user doesn't have access"""
        return redirect(url_for('index'))


class AdminModelView(ModelView):
    """ custome model view/route for the admin interface """

    def is_accessible(self):
        """ allow only admins to access the views for each database table """
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        """ redirect to index page if user doesn't have access"""
        return redirect(url_for('index'))


class AdminUserView(AdminModelView):
    """ custom view for the User table """
    column_exclude_list = ['password_hash']


class AdminAttemptView(AdminModelView):
    """ custom view for the Finished and Saved Attempt table """
    can_create = False
