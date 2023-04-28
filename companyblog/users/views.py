from flask import render_template, redirect, url_for, flash, request, Blueprint, abort
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


# Account
@users.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = form.username.data
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("User account updated")
        return redirect(url_for("users.account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename="profile_pics/"+current_user.profile_image)

    return render_template('account.html', profile_image=profile_image, form=form)


# Log Out
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# List blog posts
@users.route('/<username>')
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    stmt = db.select(User).where(User.username == username)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        abort(404)
    stmt = db.select(BlogPost).where(BlogPost.author == user).order_by(BlogPost.date.desc())
    blog_posts = db.paginate(stmt, page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)