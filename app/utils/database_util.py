from flask import abort

from app.app import db


def save_data_in_db(data):
    db.session.add(data)
    db.session.commit()


def delete_data_in_db(data):
    db.session.delete(data)
    db.session.commit()


def get_data_from_db_or_404(object_class, object_id):
    obj = db.session.get(object_class, object_id)
    if obj is None:
        abort(404, "Object not found")
    else:
        return obj
