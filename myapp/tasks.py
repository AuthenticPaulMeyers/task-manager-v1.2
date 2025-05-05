
from flask import redirect, url_for, render_template, Blueprint, request, flash
from flask_login import current_user, login_required
from .forms import TaskForm
from .models import Task
from . import db
task = Blueprint('task', __name__, url_prefix='/task-manager')

@task.route('/')
def index():
    return render_template('index.html')

@task.route('/home')
@login_required
def home():

    status_filter = request.args.get('status')
    day_filter = request.args.get('day')

    query = Task.query

    if status_filter == 'True':
        query = query.filter_by(user_id=current_user.id, is_completed=True)

    if status_filter == 'False':
        query = query.filter_by(user_id=current_user.id, is_completed=False)

    if day_filter:
        query = query.filter_by(user_id=current_user.id, reminder_day=day_filter)
    
    if status_filter == 'all':
        query = query.filter_by(user_id=current_user.id)
    
    tasks = query.order_by(Task.create_at.desc()).all()

    return render_template('home.html', title='Home', username=current_user.username, tasks=tasks)

# add taask route
@task.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        description = form.description.data
        reminder_time = form.reminder_time.data
        reminder_day = form.reminder_day.data
        complete_status = form.is_completed.data

        task = Task(title=title, description=description, reminder_time=reminder_time, reminder_day=reminder_day, is_completed=complete_status, user_id=current_user.id)

        db.session.add(task)
        db.session.commit()
        flash('New task added!', category='success')
        return redirect(url_for('task.home'))
    return render_template('add_task.html', title='Add Task', form=form)

# edit task route
@task.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):

    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    form = TaskForm(obj=task)

    if task is None:
        flash('Task not available.', category='error')
        return redirect(url_for('task.home'))

    if request.method == 'POST' and form.validate():
        task.title = form.title.data
        task.description = form.description.data
        task.reminder_time = form.reminder_time.data
        task.reminder_day = form.reminder_day.data
        task.is_completed = form.is_completed.data
        db.session.commit()

        flash('Task edited.', category='success')
        return redirect(url_for('task.home'))
    return render_template('edit_task.html', form=form, title='Edit Task', task=task)

# delete task route
@task.route('/delete_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted.", category='success')
        return redirect(url_for('task.home'))
    return redirect(url_for('task.home'))


def str_to_bool(value):
    return str(value).strip().capitalize() in ['True','False']