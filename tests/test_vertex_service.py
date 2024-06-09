import random

from app.app import db
from app.models import Vertex
from app.services import vertex_service as vertex_service
from tests import helper_test


def test_create_vertex(app):
    with app.app_context():
        # given
        x_position = random.randint(0, 500)
        y_position = random.randint(0, 500)
        # when
        created_vertex = vertex_service.create_vertex(x_position, y_position)
        # then
        assert created_vertex is not None
        assert created_vertex.x == x_position
        assert created_vertex.y == y_position


def test_delete_vertex(app):
    with (app.app_context()):
        # given
        vertex_to_delete = helper_test.get_test_vertex_in_db()
        # when
        vertex_service.delete_vertex(vertex_to_delete.id)
        # then
        assert db.session.get(Vertex, vertex_to_delete.id) is None


def test_update_vertex(app):
    with app.app_context():
        # given
        vertex_to_update = helper_test.get_test_vertex_in_db()
        new_x = random.randint(0, 500)
        new_y = random.randint(0, 500)
        # when
        vertex_service.update_vertex(vertex_to_update.id, new_x, new_y)
        # then
        updated_vertex = db.session.get(Vertex, vertex_to_update.id)
        assert updated_vertex is not None
        assert updated_vertex.x == new_x
        assert updated_vertex.y == new_y
        assert updated_vertex.id == vertex_to_update.id


def test_add_neighbor_to_vertex(app):
    with app.app_context():
        # given
        vertex = helper_test.get_test_vertex_in_db()
        neighbor = helper_test.get_test_vertex_in_db()
        # when
        vertex_service.add_neighbor_to_vertex(vertex, neighbor)
        # then
        updated_vertex = db.session.get(Vertex, vertex.id)
        assert neighbor in updated_vertex.neighbors


def test_delete_neighbor_to_vertex(app):
    with app.app_context():
        # given
        vertex = helper_test.get_test_vertex_in_db()
        neighbor = helper_test.get_test_vertex_in_db()
        vertex.neighbors.append(neighbor)
        db.session.add(vertex)
        db.session.commit()
        # when
        vertex_service.delete_neighbor_from_vertex(vertex, neighbor)
        # then
        updated_vertex = db.session.get(Vertex, vertex.id)
        assert neighbor not in updated_vertex.neighbors


def test_delete_all_neighbors_from_vertex(app):
    with app.app_context():
        # given
        vertex = helper_test.get_test_vertex_with_two_neighbors_in_db()
        # when
        vertex_service.delete_all_neighbors(vertex)
        # then
        updated_vertex = db.session.get(Vertex, vertex.id)
        assert updated_vertex.neighbors == []
