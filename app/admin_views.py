from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from flask_login import current_user
from flask_admin.base import AdminIndexView


# make admin page only accessible to admin user
class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class AdminModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('index'))


class AdminUserView(AdminModelView):
    column_exclude_list = ['password_hash']


class AdminAttemptView(AdminModelView):
    can_create = False


