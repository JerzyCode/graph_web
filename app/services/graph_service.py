from app.models import Graph, Vertex
from app.services import edge_service
from app.services import vertex_service
from app.utils import database_util as db_util
from app.utils.dto import GraphDTO


def create_empty_graph(graph_name):
    graph = Graph(graph_name)
    db_util.save_data_in_db(graph)


def delete_graph(graph_id):
    graph_to_delete = Graph.query.get_or_404(graph_id)
    db_util.delete_data_in_db(graph_to_delete)


def add_vertex_to_graph(graph_id, vertex_x, vertex_y):
    vertex_service.create_vertex(x_position=vertex_x, y_position=vertex_y, graph_id=graph_id)


def add_edge_to_graph(graph_id, vertex_in_id, vertex_out_id):
    vertex_in = Vertex.query.get_or_404(vertex_in_id)
    vertex_out = Vertex.query.get_or_404(vertex_out_id)
    graph = Graph.query.get_or_404(graph_id)
    if _check_if_graph_has_edge(graph, vertex_in, vertex_out):
        return
    edge_service.create_edge(vertex_in=vertex_in, vertex_out=vertex_out, graph_id=graph_id)
    vertex_service.add_neighbor_to_vertex(vertex_in, vertex_out)
    vertex_service.add_neighbor_to_vertex(vertex_out, vertex_in)


def get_graph_by_id(graph_id):
    graph = Graph.query.get_or_404(graph_id)
    vertices = graph.vertices.all()
    edges = graph.edges.all()
    return GraphDTO(id=graph_id, name=graph.name, vertices=vertices, edges=edges)


def _check_if_graph_has_edge(graph, vertex_in, vertex_out):
    edge = graph.edges.filter_by(vertex_in=vertex_in, vertex_out=vertex_out).first()
    return edge is not None
