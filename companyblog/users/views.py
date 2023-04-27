from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from .. import db
from .. models import User, BlogPost
from .. users.forms import RegistrationForm, LoginForm, UpdateUserForm
from .. users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)


# Registration
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.login"))
    return render_template('register.html', form=form)


# Log In
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        stmt = db.select(User).where(User.email == form.email.data)
        user = db.session.execute(stmt).scalar_one_or_none()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully")
            next = request.args.get("next")
            if next is None or not next[0] == "/":
                next = url_for("core.index")
            return redirect(next)
    return render_template("login.html", form=form)


# # Account
# @app.route('/account')
# def account():
#     return render_template('account.html')


# Log Out
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# # List blog posts
# @app.route('/blog_posts')
# def blog_posts():
#     return render_template('blog_posts.html')