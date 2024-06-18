from app.services import algorithm_service
from tests import helper_test


def test_prepare_graph(app):
    with app.app_context():
        # given
        graph = helper_test.get_test_graph_with_multiple_edges_in_db()
        # when
        prepared_graph = algorithm_service.prepare_graph(graph.id)
        # then
        prepared_vertices_ids = [vertex.id for vertex in prepared_graph.vertices]
        prepared_edges_ids = [edge.id for edge in prepared_graph.edges]
        assert prepared_graph is not None
        assert len(prepared_edges_ids) == graph.edges.count()
        for i in range(1, 11):
            assert i in prepared_vertices_ids
        for i in range(1, 7):
            assert i in prepared_edges_ids
