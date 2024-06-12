from app.models import User, Graph, Vertex
from app.services import graph_validation_service
from app.utils import database_util as db_util
from app.utils.constants import MAX_GRAPHS_PER_USER, MAX_VERTICES_PER_GRAPH
from tests import helper_test


def test_is_graph_count_exceed_should_return_true(app):
    with app.app_context():
        # given
        user = prepare_test_user()
        # when
        result = graph_validation_service.is_graph_count_exceed_by_user(user_id=user.id)
        # then
        assert result


def test_is_graph_count_exceed_should_return_false(app):
    with app.app_context():
        # given
        user = prepare_user_with_100_graphs()
        # when
        result = graph_validation_service.is_graph_count_exceed_by_user(user_id=user.id)
        # then
        assert not result


def test_is_graph_vertex_limit_exceed_should_return_true(app):
    with app.app_context():
        # given
        graph = helper_test.get_empty_test_graph_in_db()
        # when
        result = graph_validation_service.is_graph_vertex_limit_exceed(graph.id)
        # then
        assert result


def test_is_graph_vertex_limit_exceed_should_return_false(app):
    with app.app_context():
        # given
        graph = prepare_graph_with_100_vertices()
        # when
        result = graph_validation_service.is_graph_vertex_limit_exceed(graph.id)
        # then
        assert not result


def prepare_test_user():
    user = User()
    user.name = "name"
    user.email = "email@mail.com"
    user.password = "password"
    db_util.save_data_in_db(user)
    return user


def prepare_user_with_100_graphs():
    user = prepare_test_user()
    for _ in range(MAX_GRAPHS_PER_USER + 2):
        graph = Graph(name='graph', user_id=user.id)
        user.graphs.append(graph)
    return user


def prepare_graph_with_100_vertices():
    graph = helper_test.get_empty_test_graph_in_db()
    for _ in range(MAX_VERTICES_PER_GRAPH + 2):
        db_util.save_data_in_db(Vertex(graph_id=graph.id, x=0, y=0))
    return graph
