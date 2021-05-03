""" wtforms forms to be used in the flask application """

# flask-wtf
from flask_wtf import FlaskForm

# WTForms
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    """ form for user login """
    username    = StringField('Username', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """ form for user registration/sign-up """
    username = StringField('Username', validators=[
        DataRequired()
    ])

    email = StringField( 'Email', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    password_repeat = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])

    submit = SubmitField('Register')


    def validate_username(self, username):
        """ checks if username is already being used """
        username.data = username.data.strip()
        user = User.query.filter_by(username=username.data).first()

        if user is not None:
            # username already registered
            raise ValidationError("Please use a different username.")


    def validate_email(self, email):
        """ checks if email has already been registered """
        email.data = email.data.strip()
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            # email already registered
            raise ValidationError("This address has already been registered.")


class QuizForm(FlaskForm):
    """ form for the quiz questions """

    question1 = RadioField(coerce=int, validators=[DataRequired()])
    question2 = RadioField(coerce=int, validators=[DataRequired()])
    question3 = RadioField(coerce=int, validators=[DataRequired()])

    # submit button
    submit = SubmitField('Submit Test')

    # save button
    save = SubmitField('Save Test')
