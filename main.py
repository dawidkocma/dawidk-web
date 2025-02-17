import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

app = Flask(__name__)
# Get SECRET_KEY from Heroku environment variables
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY', 'fallback-secret')
ckeditor = CKEditor(app)
Bootstrap5(app)

# Use Heroku's DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')

# Fix Heroku's database URL format (Heroku uses "postgres://" but SQLAlchemy needs "postgresql://")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES

# User table for all registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

    # The "author" refers to the authors property in the BlogPost class
    posts = relationship("BlogPost", back_populates="author")

    # Refers to the comment_Author property in the Comment class
    comments = relationship("Comment", back_populates="comment_author")

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign Key, "users.id" refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # The "posts" refers to the posts property in the User class
    author = relationship("User", back_populates="posts")
    # The "parent_post" refers to Blog posts being commented by User
    comments = relationship("Comment", back_populates="parent_post", cascade="all, delete-orphan")

    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    # Child relationship to blog post
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text: Mapped[str] = mapped_column(Text, nullable=False)

with app.app_context():
    db.create_all()

# Flask-Login user loader callback
@login_manager.user_loader
def load_user(user_id):
    # Use session.get which returns None if not found
    return db.session.get(User, int(user_id))

# Admin-only decorator
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Ensure the user is authenticated and has admin rights (id == 1)
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_function

# Register route with password hashing and duplicate email check
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("This email already exists! Log in instead.")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256:600000',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()

        # Authenticate user with Flask-Login
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)

# Login route with user retrieval and password check
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("Email or password incorrect. Try again")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("get_all_posts"))
    return render_template("login.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    # Add comment form
    comment_form = CommentForm()
    # Only allow logged-in users to comment on posts
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.body.data,
            comment_author=current_user,
            parent_post=requested_post

        )
        db.session.add(new_comment)
        db.session.commit()

    return render_template("post.html", post=requested_post, current_user=current_user, form=comment_form)

# Admin-only: Create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,  # store the user's name as a string
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)

# Admin-only: Edit an existing post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user.name  # update with the current user's name
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)

# Admin-only: Delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)

# @app.route("/contact")
# def contact():
#     return render_template("contact.html", current_user=current_user)

if __name__ == "__main__":
    app.run(debug=False, port=5002)
