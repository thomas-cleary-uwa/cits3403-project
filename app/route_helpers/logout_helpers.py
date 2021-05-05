""" helper functions for the logout route """

from flask import redirect, flash
from flask_login import logout_user


def attempt_logout(flash_message="Unable to logout", redirect_route="index"):
    """ try to log user out and send them to redirect_route,
        else flash error and send to index page
    """

    try:
        logout_user()
        return redirect(redirect_route)
    except:
        flash(flash_message)
        return redirect("index")
