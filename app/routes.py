from flask import render_template
from app import app

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

    