from ..models import User
from .. import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("pw_confirm")])
    pw_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    @staticmethod
    def check_email(self, field):
        stmt = db.select(User).where(User.email == field.data)
        if db.session.execute(stmt).first():
            raise ValidationError("Your email has already been registered")

    @staticmethod
    def check_username(self, field):
        stmt = db.select(User).where(User.username == field.data)
        if db.session.execute(stmt).first():
            raise ValidationError("Your username has already been registered")


class UpdateUserForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Upload a profile picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Update")

    @staticmethod
    def check_email(self, field):
        stmt = db.select(User).where(User.email == field.data)
        if db.session.execute(stmt).first():
            raise ValidationError("Your email has already been registered")

    @staticmethod
    def check_username(self, field):
        stmt = db.select(User).where(User.username == field.data)
        if db.session.execute(stmt).first():
            raise ValidationError("Your username has already been registered")