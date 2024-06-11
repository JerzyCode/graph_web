from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = db.session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.main_graph_panel'))


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password_again = request.form.get('password-again')

    user = db.session.query(User).filter_by(email=email).first()
    if user or password_again != password:
        flash('Email address already exists')
        return redirect(url_for('main.welcome_page'))

    new_user = User()
    new_user.email = email
    new_user.name = name
    new_user.password = generate_password_hash(password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.welcome_page'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.welcome_page"))
