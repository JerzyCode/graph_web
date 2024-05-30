import random

from app.models import Graph, Vertex, Edge, GraphDTO
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


def test_add_vertex_to_graph(app):
    with app.app_context():
        # given
        vertex_x = random.randint(0, 500)
        vertex_y = random.randint(0, 500)
        graph = helper.get_empty_test_graph_in_db()
        # when
        graph_service.add_vertex_to_graph(graph_id=graph.id, vertex_x=vertex_x, vertex_y=vertex_y)
        # then
        updated_graph = Graph.query.get(graph.id)
        added_vertex = updated_graph.vertices.first()
        assert updated_graph is not None
        assert updated_graph.vertices.count() == 1
        assert added_vertex is not None
        assert added_vertex.x == vertex_x
        assert added_vertex.y == vertex_y


def test_add_edge_with_no_exist_edge(app):
    with app.app_context():
        # given
        graph = helper.get_empty_test_graph_in_db()
        edge_count_before = graph.edges.count()
        vertex_in = helper.get_test_vertex_with_graph_id_in_db(graph_id=graph.id)
        vertex_out = helper.get_test_vertex_with_graph_id_in_db(graph_id=graph.id)
        # when
        graph_service.add_edge_to_graph(graph_id=graph.id, vertex_in_id=vertex_in.id, vertex_out_id=vertex_out.id)
        # then
        updated_graph = Graph.query.get(graph.id)
        updated_vertex_in = Vertex.query.get(vertex_in.id)
        updated_vertex_out = Vertex.query.get(vertex_out.id)
        added_edge = updated_graph.edges.first()
        assert updated_graph is not None
        assert added_edge is not None
        assert updated_graph.vertices.count() == 2
        assert updated_graph.edges.count() == edge_count_before + 1
        assert updated_vertex_out in updated_vertex_in.neighbors
        assert updated_vertex_in in updated_vertex_out.neighbors


def test_add_edge_to_graph_with_exist_edge(app):
    with app.app_context():
        # given
        graph = helper.get_test_graph_with_edges_in_db()
        edge_count_before = graph.edges.count()
        existing_edge = graph.edges.first()
        vertex_in = existing_edge.vertex_in
        vertex_out = existing_edge.vertex_out
        # when
        graph_service.add_edge_to_graph(graph_id=graph.id, vertex_in_id=vertex_in.id, vertex_out_id=vertex_out.id)
        # then
        updated_graph = Graph.query.get(graph.id)
        assert updated_graph is not None
        assert updated_graph.vertices.count() == 2
        assert updated_graph.edges.count() == edge_count_before


def test_get_graph(app):
    with app.app_context():
        # given
        graph = helper.get_test_graph_with_edges_in_db()
        # when
        result = graph_service.get_graph_by_id(graph.id)
        print(result.map_to_dictionary())
        # then
        assert result is not None
        assert isinstance(result, GraphDTO)
        assert result.vertices == graph.vertices.all()
        assert result.edges == graph.edges.all()
        assert result.id == graph.id
        assert result.name == graph.name
