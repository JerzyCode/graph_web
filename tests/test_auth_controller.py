from unittest.mock import patch

from flask import url_for

from app.utils.constants import WELCOME_PAGE_URL, GRAPH_PANEL_URL
from app.utils.exceptions import EmailTakenException, InvalidPasswordException, PasswordsDoNotMatchException

SIGNUP_REQUEST_DATA = {
    'email': 'test@example.com',
    'name': 'Test User',
    'password': 'password123',
    'password-again': 'password123'
}

LOGIN_REQUEST_DATA = {
    'email': 'test@example.com',
    'password': 'password123',
    'remember': 'true'
}


def test_signup_request_should_redirect(app, client):
    # given
    # when
    with patch('app.services.auth_service.create_new_user') as auth_service:
        response = client.post('/signup', data=SIGNUP_REQUEST_DATA)

    # then
    assert response.status_code == 302
    with app.app_context():
        assert response.location == url_for(WELCOME_PAGE_URL, _external=False)
    auth_service.assert_called_once()


def test_signup_request_email_taken_exception_should_redirect(app, client):
    # given
    # when
    with patch('app.services.auth_service.create_new_user', side_effect=EmailTakenException) as auth_service:
        response = client.post('/signup', data=SIGNUP_REQUEST_DATA)

    # then
    assert response.status_code == 302
    with app.app_context():
        assert response.location == url_for(WELCOME_PAGE_URL, _external=False)
    auth_service.assert_called_once()


def test_signup_request_invalid_passwords_exception_should_redirect(app, client):
    # given
    # when
    with patch('app.services.auth_service.create_new_user', side_effect=InvalidPasswordException) as auth_service:
        response = client.post('/signup', data=SIGNUP_REQUEST_DATA)

    # then
    assert response.status_code == 302
    with app.app_context():
        assert response.location == url_for(WELCOME_PAGE_URL, _external=False)
    auth_service.assert_called_once()


def test_login_request_should_redirect(app, client):
    # given
    # when
    with patch('app.services.auth_service.login_user_req') as auth_service:
        response = client.post('/login', data=LOGIN_REQUEST_DATA)

    # then
    assert response.status_code == 302
    with app.app_context():
        assert response.location == url_for(GRAPH_PANEL_URL, _external=False)
    auth_service.assert_called_once()


def test_login_request_wrong_password_exception_should_redirect(app, client):
    # given
    # when
    with patch('app.services.auth_service.login_user_req', side_effect=PasswordsDoNotMatchException) as auth_service:
        response = client.post('/login', data=LOGIN_REQUEST_DATA)

    # then
    assert response.status_code == 302
    with app.app_context():
        assert response.location == url_for(WELCOME_PAGE_URL, _external=False)
    auth_service.assert_called_once()
