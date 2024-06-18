import random
from unittest.mock import MagicMock

from werkzeug.security import generate_password_hash

from app.app import db
from app.models import Vertex, Graph, Edge, User

TEST_USER_ID = random.randint(0, 5000)
TEST_USER_PASSWORD = 'test_password'


def get_test_vertex_no_db():
    x_position = random.randint(0, 500)
    y_position = random.randint(0, 500)
    return Vertex(x_position, y_position)


def get_test_vertex_in_db():
    vertex = get_test_vertex_no_db()
    db.session.add(vertex)
    db.session.commit()
    return db.session.get(Vertex, vertex.id)


def get_test_vertex_with_graph_id_in_db(graph_id):
    vertex = get_test_vertex_no_db()
    vertex.graph_id = graph_id
    db.session.add(vertex)
    db.session.commit()
    return db.session.get(Vertex, vertex.id)


def get_empty_test_graph_in_db():
    new_user = User()
    new_user.id = TEST_USER_ID
    new_user.email = 'testmail'
    new_user.name = 'testname'
    new_user.password = TEST_USER_PASSWORD
    db.session.add(new_user)

    graph = Graph(name="test_graph" + str(random.randint(0, 10000)), user_id=1)
    graph.user_id = new_user.id
    db.session.add(graph)
    db.session.commit()
    return db.session.query(Graph).filter_by(name=graph.name).first()


def _get_test_edge_with_graph_id_in_db(vertex_in, vertex_out, graph_id):
    edge = Edge(vertex_in, vertex_out, graph_id=graph_id)
    db.session.add(edge)
    db.session.commit()
    db.session.get(Edge, edge.id)
    return db.session.get(Edge, edge.id)


def get_test_edge_with_vertices_in_db():
    vertex_in = get_test_vertex_in_db()
    vertex_out = get_test_vertex_in_db()
    return _get_test_edge_with_graph_id_in_db(vertex_in, vertex_out, graph_id=None)


def get_test_graph_with_edges_in_db():
    graph = get_empty_test_graph_in_db()
    vertex_in = get_test_vertex_with_graph_id_in_db(graph.id)
    vertex_out = get_test_vertex_with_graph_id_in_db(graph.id)
    edge = _get_test_edge_with_graph_id_in_db(vertex_in, vertex_out, graph.id)

    vertex_in.neighbors.append(vertex_out)
    vertex_out.neighbors.append(vertex_in)

    graph.vertices.append(vertex_in)
    graph.vertices.append(vertex_out)

    graph.edges.append(edge)

    db.session.add_all([vertex_in, vertex_out, graph])
    db.session.commit()
    return db.session.get(Graph, graph.id)


def get_test_graph_with_multiple_edges_in_db():
    graph = get_empty_test_graph_in_db()

    vertices = [get_test_vertex_with_graph_id_in_db(graph.id) for _ in range(10)]
    graph.vertices.extend(vertices)

    edges_data = [
        (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (2, 6)
    ]
    edges = []
    for source_idx, target_idx in edges_data:
        source_vertex = vertices[source_idx]
        target_vertex = vertices[target_idx]
        edge = _get_test_edge_with_graph_id_in_db(source_vertex, target_vertex, graph.id)
        edges.append(edge)
        source_vertex.neighbors.append(target_vertex)
        target_vertex.neighbors.append(source_vertex)

    graph.edges.extend(edges)

    db.session.add_all(vertices + edges + [graph])
    db.session.commit()

    return db.session.get(Graph, graph.id)


def get_test_vertex_with_two_neighbors_in_db():
    vertex = get_test_vertex_in_db()
    first_neigh = get_test_vertex_in_db()
    second_neigh = get_test_vertex_in_db()
    vertex.neighbors.append(first_neigh)
    vertex.neighbors.append(second_neigh)
    db.session.add(vertex)
    db.session.commit()
    return db.session.get(Vertex, vertex.id)


def prepare_test_user_no_db():
    user = User()
    user.email = 'test@mail.com'
    user.name = 'name'
    user.password = generate_password_hash(TEST_USER_PASSWORD)
    return user


def prepare_test_user_in_db():
    user = prepare_test_user_no_db()
    db.session.add(user)
    db.session.commit()
    return user


def get_mock_user():
    mock_user = MagicMock()
    mock_user.id = TEST_USER_ID
    return mock_user
