
from flask import redirect, url_for, render_template, Blueprint, request, flash
from flask_login import current_user, login_required
from .forms import TaskForm
from .models import Task
from . import db
# from myapp.taskscheduler.scheduler import send_reminder 

task = Blueprint('task', __name__, url_prefix='/task-manager')

# the root
@task.route('/')
def index():
    return render_template('index.html', user=current_user)

# display all task
@task.route('/tasks')
@login_required
def home():

    status_filter = request.args.get('status')
    day_filter = request.args.get('day')

    query = Task.query.filter_by(user_id=current_user.id)

    if status_filter == 'True':
        query = query.filter_by(is_completed=True)

    if status_filter == 'False':
        query = query.filter_by(is_completed=False)

    if day_filter:
        query = query.filter_by(reminder_day=day_filter)
    
    if status_filter == 'all':
        query = query.filter_by(user_id=current_user.id)
    
    tasks = query.order_by(Task.create_at.desc()).all()

    return render_template('home.html', title='Home', user=current_user, tasks=tasks)

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

        # # Schedule email
        # eta = task.reminder_time  # datetime object
        # send_reminder.apply_async(
        #     args=[current_user.email, "Task Reminder", f"Reminder: {task.title}"],
        #     eta=eta  # executes at exact reminder_time
        # )

        flash('New task added!', category='success')
        return redirect(url_for('task.home'))
    return render_template('add_task.html', title='Add Task', form=form, user=current_user)

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

        
        # # Schedule email
        # eta = task.reminder_time  # datetime object
        # send_reminder.apply_async(
        #     args=[current_user.email, "Task Reminder", f"Reminder: {task.title}"],
        #     eta=eta  # executes at exact reminder_time
        # )

        flash('Task edited.', category='success')
        return redirect(url_for('task.home'))
    return render_template('edit_task.html', form=form, title='Edit Task', task=task, user=current_user)

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

