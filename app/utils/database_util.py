from app.app import db


def save_data_in_db(data):
    db.session.add(data)
    db.session.commit()


def delete_data_in_db(data):
    db.session.delete(data)
    db.session.commit()
