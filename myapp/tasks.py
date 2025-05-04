
from flask import redirect, url_for, render_template, Blueprint
from flask_login import current_user, login_required

task = Blueprint('task', __name__, url_prefix='/task')

@task.route('/')
def index():
    return 'index route'


@task.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home', username=current_user.username)
