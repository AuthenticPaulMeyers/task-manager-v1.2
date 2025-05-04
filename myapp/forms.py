from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, TimeField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class RegistrationForm(FlaskForm):
    username = StringField("Username", [Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    email = StringField("Email", [Length(min=4, max=90), Email()], render_kw={"placeholder": "name@example.com"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Create password"})
    confirm = PasswordField("Confirm", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "name@example.com"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Create password"})
    submit = SubmitField("Login")


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Project title"})
    description = TextAreaField("Description", validators=[DataRequired()], render_kw={"placeholder": "Project description"})
    reminder_time = TimeField("Set reminder", validators=[DataRequired()], render_kw={"placeholder": "Set reminder time"})
    reminder_day = SelectField('Select a Day', choices=[
        ('Monday'),
        ('Tuesday'),
        ('Wednesday'),
        ('Thursday'),
        ('Friday'),
        ('Saturday'),
        ('Sunday')
    ])
    is_completed = BooleanField("Completed")
    submit = SubmitField('Submit task')