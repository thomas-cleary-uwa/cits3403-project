from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Thomas'}

    jobs = [
        {
            'person' : {'name' : 'Thomas'},
            'task' : 'login'
        },
        {
            'person' : {'name' : 'Calvin'},
            'task' : 'content'
        },
        {
            'person' : {'name' : 'Jason'},
            'task' : 'home page'
        },
        {
            'person' : {'name' : 'Michael'},
            'task' : 'quiz'
        }
    ]

    return render_template('index.html', user=user, jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)