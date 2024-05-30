import random

from app.app import db
from app.models import Vertex


def get_test_vertex_no_db():
    x_position = random.randint(0, 500)
    y_position = random.randint(0, 500)
    return Vertex(x_position, y_position)


def get_test_vertex_in_db():
    vertex = get_test_vertex_no_db()
    db.session.add(vertex)
    db.session.commit()
    return Vertex.query.get(vertex.id)
