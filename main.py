from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MY_DATABASE_URL')
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)
Bootstrap(app)


# to track users logins
login_manager = LoginManager()
login_manager.init_app(app)


# charger un utilisateur à partir de la base de données en utilisant son identifiant
# loading the current user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Create admin-only decorator
def admin_only(fa):
    @wraps(fa)  # pour préserver le nom et la documentation de la fonction originale dans la fonction décorée
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return fa(*args, **kwargs)

    return decorated_function


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', back_populates='author', lazy=True)
    comments = db.relationship('Comment', back_populates='commenter', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', back_populates='posts')  # Include the User object
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', back_populates="parent_post", lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commenter = db.relationship('User', back_populates='comments')  # Include the User object

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_post = db.relationship('Post', back_populates='comments')  # Include the Post object


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    if not hasattr(index, 'is_called'):
        # First time the function is called
        setattr(index, 'is_called', True)
        user = None
    else:
        user = current_user
    return render_template('index.html', current_user=user)

# ****************************  USER   ****************************


@app.route('/login', methods=['GET', 'POST'])
def login():  # login
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        user = User.query.filter_by(name=name).first()
        # Name doesn't exist
        if not user:
            flash("Ce Pseudo n'existe pas, veuillez réessayer.")
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Mot de passe incorrect, veuillez réessayer.')
        else:
            login_user(user)
            return redirect(url_for('get_posts'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')  # logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/contact")
def contact():
    users = User.query.all()
    return render_template("contact.html",
                           current_user=current_user,
                           users=users,
                           number_user=User.query.count(),
                           number_comment=Comment.query.count(),
                           number_post=Post.query.count())


@app.route("/setting")
def setting():
    return render_template("Settings.html", current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        if User.query.filter_by(name=form.name.data).first():
            flash("Pseudo non disponible, déjà pris.")
            return redirect(url_for('register'))
        new_user = User(
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        return redirect(url_for('get_posts'))
    return render_template("register.html", form=form, current_user=current_user, edit=False)


@app.route("/edit-user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if user_id == 1:
        return redirect(url_for('get_posts'))
    if current_user.id != 1 and current_user.id != user_id:
        return redirect(url_for('get_posts'))
    user_to_edit = User.query.get(user_id)
    form = RegisterForm(
        name=user_to_edit.name,
        password=user_to_edit.password
    )
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        user_to_edit.name = form.name.data
        user_to_edit.password = hash_and_salted_password
        db.session.commit()
        logout_user()  # you first log out the actual user
        # Log in and authenticate user after adding details to database.
        login_user(user_to_edit)
        return redirect(url_for('get_posts'))
    return render_template("register.html", form=form, current_user=current_user, edit=True)


@app.route("/delete-user/<int:user_id>")
@login_required
def delete_user(user_id):
    if user_id == 1:
        return redirect(url_for('get_posts'))
    if user_id == current_user.id or current_user.id == 1:
        user_to_delete = User.query.get(user_id)
        # deleting all the comments of the user to delete
        for comment in Comment.query.filter_by(commenter=user_to_delete).all():
            db.session.delete(comment)
            db.session.commit()
        # deleting all the posts of the user
        for the_post in Post.query.filter_by(author=user_to_delete).all():
            # deleting all comments of each post
            for comment in Comment.query.filter_by(parent_post=the_post).all():
                db.session.delete(comment)
                db.session.commit()
            db.session.delete(the_post)
            db.session.commit()
        db.session.delete(user_to_delete)
        db.session.commit()
    return redirect(url_for('get_posts'))


@app.route("/reset-user/<int:user_id>")
@admin_only  # only Admins will reset
def reset_user(user_id):
    if user_id == 1:
        return redirect(url_for('get_posts'))
    user = User.query.get(user_id)
    hash_and_salted_password = generate_password_hash(
        '0000',
        method='pbkdf2:sha256',
        salt_length=8
    )
    user.password = hash_and_salted_password
    db.session.commit()
    return redirect(url_for('get_posts'))


# ****************************  POST   ****************************


@app.route('/posts')  # get all posts
@login_required
def get_posts():
    posts = Post.query.all()
    return render_template('all_posts.html', posts=posts, current_user=current_user)


@app.route('/post/<int:post_id>')  # get one post
@login_required
def post(post_id):
    if post_id == 0:
        posts = Post.query.count()
        return render_template('refresh.html', posts=posts)
    the_post = Post.query.get(post_id)
    comments = the_post.comments
    return render_template('post.html', post=the_post, comments=comments, current_user=current_user)


@socketio.on('post')  # emit when new post added
def handle_post(post_data):
    new_post = Post(title=post_data['title'], subtitle=post_data['subtitle'], user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    # Emit a Socket.IO event for new posts
    socketio.emit('post', {
        'title': new_post.title,
        'subtitle': new_post.subtitle,
        'timestamp': new_post.timestamp.strftime('%Y-%m-%d %H:%M')
    })


# ***************************** COMMENTS *****************


@socketio.on('comment')
def handle_comment(comment_data):
    post_id = comment_data.get('post_id')  # Use get to avoid KeyError
    the_post = Post.query.get(post_id)

    if the_post:
        new_comment = Comment(content=comment_data['content'],
                              parent_post=the_post,
                              user_id=current_user.id,
                              post_id=the_post.id)
        db.session.add(new_comment)
        db.session.commit()

        # Emit a Socket.IO event for new comments
        socketio.emit('comment', {
            'content': new_comment.content,
            'timestamp': new_comment.timestamp.strftime('%Y-%m-%d %H:%M'),
            'post_id': post_id
        })


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

