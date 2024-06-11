from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.app import db
from app.models import User
from app.utils.constants import WELCOME_PAGE_URL

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = db.session.query(User).filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('login-flash')
        return redirect(url_for(WELCOME_PAGE_URL))

    login_user(user, remember=remember)

    return redirect(url_for('main.main_graph_panel'))


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password_again = request.form.get('password-again')

    user = db.session.query(User).filter_by(email=email).first()

    if user:
        flash('signup-email-taken-flash')
        return redirect(url_for(WELCOME_PAGE_URL))

    if password != password_again:
        flash('signup-password-do-not-match')
        return redirect(url_for(WELCOME_PAGE_URL))

    new_user = User()
    new_user.email = email
    new_user.name = name
    new_user.password = generate_password_hash(password)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for(WELCOME_PAGE_URL))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(WELCOME_PAGE_URL))
