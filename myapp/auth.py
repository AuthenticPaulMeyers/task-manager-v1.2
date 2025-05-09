
from flask import flash, redirect, url_for, render_template, request
from flask import redirect, url_for, render_template, Blueprint
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from myapp.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    from .models import User
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # check if the user already exists
        if User.query.filter_by(email=email).first():
            flash('User already exist!', category='error')
            return redirect(url_for('auth.register'))
        
        # hash the user password
        password_hashed = generate_password_hash(password)

        user = User(username=username, email=email, password=password_hashed)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!', category='success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, title='Register', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    from .models import User
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('task.home'))
            flash('Wrong email or password', category='error')
        # flash('Wrong email or password', category='error')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html', form=form, title='Login', user=current_user)

@auth.get('/profile')
@login_required
def get_profile():
    from .models import User

    user_profile = User.query.filter_by(id=current_user.id).first()

    return render_template('profile.html', title='Profile', user_profile=user_profile, user=current_user)

@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('task.index'))