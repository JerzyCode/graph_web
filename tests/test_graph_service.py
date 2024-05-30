from app.models import Graph, Vertex, Edge

from app.services import graph_service
from tests import helper


def test_create_graph(app):
    with app.app_context():
        # given
        graph_name = 'test_graph'
        # when
        graph_service.create_empty_graph(graph_name)
        # then
        saved_graph = Graph.query.filter_by(name=graph_name).first()
        assert saved_graph is not None
        assert saved_graph.edges.count() == 0
        assert saved_graph.vertices.count() == 0


def test_delete_empty_graph(app):
    with app.app_context():
        # given
        graph_to_delete = helper.get_empty_test_graph_in_db()
        # when
        graph_service.delete_graph(graph_to_delete.id)
        # then
        deleted = Graph.query.filter_by(name=graph_to_delete.name).first()
        assert deleted is None


def test_delete_graph_with_edges(app):
    with app.app_context():
        # given
        graph_to_delete = helper.get_test_graph_with_edges_in_db()
        # when
        graph_service.delete_graph(graph_to_delete.id)
        # then
        deleted_graph = Graph.query.get(graph_to_delete.id)
        assert deleted_graph is None
        assert Vertex.query.filter_by(graph_id=graph_to_delete.id).count() == 0
        assert Edge.query.filter_by(graph_id=graph_to_delete.id).count() == 0
