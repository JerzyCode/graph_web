from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.app import db
from app.models import User
from app.utils.exceptions import EmailTakenException, InvalidPasswordException, PasswordsDoNotMatchException


def create_new_user(email: str, name: str, password: str, password_again: str):
    _validate_create_user(email, password, password_again)

    new_user = User()
    new_user.email = email
    new_user.name = name
    new_user.password = generate_password_hash(password)

    db.session.add(new_user)
    db.session.commit()


def _validate_create_user(email: str, password: str, password_again: str):
    if not _is_valid_email(email):
        raise EmailTakenException
    if not _is_passwords_the_same(password, password_again):
        raise InvalidPasswordException


def _is_valid_email(email: str):
    if len(email) < 4 or '@' not in email:
        return False
    existing_user = db.session.query(User).filter_by(email=email).first()
    return existing_user is None


def _is_passwords_the_same(password: str, password_again: str):
    if len(password) < 8:
        return False
    return password == password_again


def login_user_req(email: str, password: str, remember_me: bool):
    user = db.session.query(User).filter_by(email=email).first()

    if not _is_valid_password(user.password, password):
        print('Invalid password')
        raise PasswordsDoNotMatchException

    login_user(user, remember=remember_me)


def _is_valid_password(user_password: str, entered_password: str):
    return check_password_hash(user_password, entered_password)
