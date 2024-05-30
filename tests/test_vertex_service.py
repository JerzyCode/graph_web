import random

from app.app import db
from app.models import Vertex
from app.services import vertex_service as vertex_service


def get_test_vertex_no_db():
    x_position = random.randint(0, 500)
    y_position = random.randint(0, 500)
    return Vertex(x_position, y_position)


def get_test_vertex_in_db():
    vertex = get_test_vertex_no_db()
    db.session.add(vertex)
    db.session.commit()
    return Vertex.query.get(vertex.id)


def test_save_vertex(app):
    with app.app_context():
        # given
        x_position = random.randint(0, 500)
        y_position = random.randint(0, 500)
        # when
        vertex_service.save_vertex(x_position, y_position)
        # then
        saved_vertex = Vertex.query.first()
        assert saved_vertex is not None
        assert saved_vertex.x == x_position
        assert saved_vertex.y == y_position


def test_delete_vertex(app):
    with app.app_context():
        # given
        vertex_to_delete = get_test_vertex_in_db()
        # when
        vertex_service.delete_vertex(vertex_to_delete.id)
        # then
        assert Vertex.query.get(vertex_to_delete.id) is None


def test_update_vertex(app):
    with app.app_context():
        # given
        vertex_to_update = get_test_vertex_in_db()
        new_x = random.randint(0, 500)
        new_y = random.randint(0, 500)
        # when
        vertex_service.update_vertex(vertex_to_update.id, new_x, new_y)
        # then
        updated_vertex = Vertex.query.get(vertex_to_update.id)
        assert updated_vertex is not None
        assert updated_vertex.x == new_x
        assert updated_vertex.y == new_y
        assert updated_vertex.id == vertex_to_update.id


def test_add_neighbor_to_vertex(app):
    with app.app_context():
        # given
        vertex = get_test_vertex_in_db()
        neighbor = get_test_vertex_in_db()
        # when
        vertex_service.add_neighbor_to_vertex(vertex, neighbor)
        # then
        assert neighbor in vertex.neighbors
