import pytest

from app.app import create_app, db

db_url = 'sqlite:///test.db'


@pytest.fixture()
def app():
    app = create_app(db_url)

    with app.app_context():
        db.create_all()

    yield app
