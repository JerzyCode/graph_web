import pytest

from app.app import create_app, db

db_url = 'sqlite:///'


@pytest.fixture()
def app():
    app = create_app(db_url)

    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['LOGIN_DISABLED'] = True
    app.config['SERVER_NAME'] = 'localhost'

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
