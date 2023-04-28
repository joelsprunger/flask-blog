from flask import render_template, url_for, redirect, flash, request, Blueprint, abort
from flask_login import current_user, login_required
from .. import db
from .. models import BlogPost
from .. blog_posts.forms import BlogPostForm

blog_posts = Blueprint("blog_posts", __name__)


# CREATE
@blog_posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(title=form.title.data,
                        text=form.text.data,
                        user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("core.index"))
    return render_template("create_post.html", form=form)


# READ (View)
@blog_posts.route("/<int:blog_post_id>")
def blog_post(blog_post_id):
    stmt = db.select(BlogPost).where(BlogPost.id == blog_post_id)
    blog_post = db.session.execute(stmt).scalar_one_or_none()
    if blog_post is None:
        abort(404)
    return render_template("blog_post.html",
                           title=blog_post.title,
                           date=blog_post.date.strftime("%Y-%m-%d"),
                           post=blog_post)


# UPDATE
@blog_posts.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update(blog_post_id):
    stmt = db.select(BlogPost).where(BlogPost.id == blog_post_id)
    blog_post = db.session.execute(stmt).scalar_one_or_none()
    if blog_post is None:
        abort(404)
    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        return redirect(url_for("blog_posts.blog_post", blog_post_id=blog_post.id))
    elif request.method == "GET":
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template("create_post.html", form=form, title='Updating')


# DELETE
@blog_posts.route("/<int:blog_post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(blog_post_id):
    stmt = db.select(BlogPost).where(BlogPost.id == blog_post_id)
    blog_post = db.session.execute(stmt).scalar_one_or_none()
    if blog_post is None:
        abort(404)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    return redirect(url_for("core.index"))
