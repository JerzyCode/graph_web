from unittest.mock import patch

import pytest

from app.models import User
from app.services import auth_service
from app.utils.exceptions import EmailTakenException, InvalidPasswordException, PasswordsDoNotMatchException
from tests.helper_test import prepare_test_user_no_db, prepare_test_user_in_db, TEST_USER_PASSWORD


def test_create_user_should_create_new_user(app):
    with app.app_context():
        # given
        user_data = prepare_test_user_no_db()
        password_again = user_data.password
        # when
        auth_service.create_new_user(email=user_data.email, name=user_data.name,
                                     password=user_data.password, password_again=password_again)
        # then
        created_user = User.query.filter_by(email=user_data.email).first()
        assert created_user is not None
        assert created_user.email == user_data.email
        assert created_user.name == user_data.name
        assert created_user.password is not None


def test_create_user_should_throw_username_taken_exception(app):
    with app.app_context():
        # given
        saved_user = prepare_test_user_in_db()
        email = saved_user.email
        name = 'name'
        password = 'testpassword'
        password_again = 'testpassword'
        # when & then
        with pytest.raises(EmailTakenException):
            auth_service.create_new_user(email=email, name=name, password=password, password_again=password_again)


def test_create_user_to_short_password_should_throw_invalid_password_exception(app):
    with app.app_context():
        # given
        user_data = prepare_test_user_no_db()
        user_data.password = '123'
        password_again = user_data.password
        # when & then
        with pytest.raises(InvalidPasswordException):
            auth_service.create_new_user(email=user_data.email, name=user_data.name,
                                         password=user_data.password, password_again=password_again)


def test_create_user_different_password_should_throw_invalid_password_exception(app):
    with app.app_context():
        # given
        user_data = prepare_test_user_no_db()
        password_again = user_data.password + 'changing password'
        # when & then
        with pytest.raises(InvalidPasswordException):
            auth_service.create_new_user(email=user_data.email, name=user_data.name,
                                         password=user_data.password, password_again=password_again)


def test_should_login_user_with_correct_credentials(app):
    with app.app_context():
        # given
        remember_me = True
        no_hashed_password = TEST_USER_PASSWORD
        saved_user = prepare_test_user_in_db()

        # when
        with patch('app.services.auth_service.login_user') as login_user_mock:
            auth_service.login_user_req(saved_user.email, no_hashed_password, remember_me=remember_me)
        # then
        login_user_mock.assert_called_once_with(saved_user, remember=remember_me)


def test_should_login_user_with_incorrect_credentials_should_throw(app):
    with app.app_context():
        # given
        remember_me = True
        no_hashed_password = TEST_USER_PASSWORD + 'changed'
        saved_user = prepare_test_user_in_db()

        # when & then
        with pytest.raises(PasswordsDoNotMatchException):
            with patch('app.services.auth_service.login_user') as login_user_mock:
                auth_service.login_user_req(saved_user.email, no_hashed_password, remember_me=remember_me)
                login_user_mock.assert_not_called(saved_user, remember=remember_me)
