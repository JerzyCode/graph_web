from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_required, logout_user

from app.services import auth_service
from app.utils.constants import WELCOME_PAGE_URL, GRAPH_PANEL_URL
from app.utils.exceptions import EmailTakenException, InvalidPasswordException, PasswordsDoNotMatchException

auth_bp = Blueprint('auth', __name__)


class AuthController:

    @staticmethod
    def handle_signup_request(signup_request):
        email = signup_request.form.get('email')
        name = signup_request.form.get('name')
        password = signup_request.form.get('password')
        password_again = signup_request.form.get('password-again')
        try:
            auth_service.create_new_user(email, name, password, password_again)
        except EmailTakenException:
            flash('signup-email-taken-flash')
            return redirect(url_for(WELCOME_PAGE_URL))
        except InvalidPasswordException:
            flash('signup-password-do-not-match')
            return redirect(url_for(WELCOME_PAGE_URL))
        return redirect(url_for(WELCOME_PAGE_URL))

    @staticmethod
    def handle_login_request(login_request):
        email = login_request.form.get('email')
        password = login_request.form.get('password')
        remember = True if request.form.get('remember') else False
        try:
            auth_service.login_user_req(email, password, remember)
        except PasswordsDoNotMatchException:
            flash('login-flash')
            return redirect(url_for(WELCOME_PAGE_URL))
        return redirect(url_for(GRAPH_PANEL_URL))


auth_controller = AuthController()


@auth_bp.route('/login', methods=['POST'])
def login_post():
    return auth_controller.handle_login_request(request)


@auth_bp.route('/signup', methods=['POST'])
def signup_post():
    return auth_controller.handle_signup_request(request)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(WELCOME_PAGE_URL))
