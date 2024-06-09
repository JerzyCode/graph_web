import pytest

from app.app import create_app, db

db_url = 'sqlite:///'


@pytest.fixture()
def app():
    app = create_app(db_url)

    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
