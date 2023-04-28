from flask import render_template, request, Blueprint
from .. import db
from .. models import BlogPost

core = Blueprint("core", __name__)


@core.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    stmt = db.select(BlogPost).order_by(BlogPost.date.desc())
    blog_posts = db.paginate(stmt, page=page, per_page=10)
    return render_template("index.html", blog_posts=blog_posts)


@core.route("/info")
def info():
    return render_template("info.html")
