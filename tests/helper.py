import random

from app.app import db
from app.models import Vertex, Graph, Edge


def get_test_vertex_no_db():
    x_position = random.randint(0, 500)
    y_position = random.randint(0, 500)
    return Vertex(x_position, y_position)


def get_test_vertex_in_db():
    vertex = get_test_vertex_no_db()
    db.session.add(vertex)
    db.session.commit()
    return Vertex.query.get(vertex.id)


def get_test_vertex_with_graph_id_in_db(graph_id):
    vertex = get_test_vertex_no_db()
    vertex.graph_id = graph_id
    db.session.add(vertex)
    db.session.commit()
    return Vertex.query.get(vertex.id)


def get_empty_test_graph_in_db():
    graph = Graph(name="test_graph" + str(random.randint(0, 10000)))
    db.session.add(graph)
    db.session.commit()
    return Graph.query.filter_by(name=graph.name).first()


def _get_test_edge_with_graph_id_in_db(vertex_in, vertex_out, graph_id):
    edge = Edge(vertex_in, vertex_out, graph_id=graph_id)
    db.session.add(edge)
    db.session.commit()
    return Edge.query.get(edge.id)


def get_test_graph_with_edges_in_db():
    graph = get_empty_test_graph_in_db()
    vertex_in = get_test_vertex_with_graph_id_in_db(graph.id)
    vertex_out = get_test_vertex_with_graph_id_in_db(graph.id)
    edge = _get_test_edge_with_graph_id_in_db(vertex_in, vertex_out, graph.id)

    graph.vertices.append(vertex_in)
    graph.vertices.append(vertex_out)

    graph.edges.append(edge)

    db.session.add(graph)
    db.session.commit()
    return Graph.query.get(graph.id)
