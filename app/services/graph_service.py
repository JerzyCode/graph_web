from app.models import Graph, Vertex, Edge
from app.services import edge_service
from app.services import graph_validation_service as validator
from app.services import vertex_service
from app.utils import database_util as db_util
from app.utils.classes import GraphDTO
from app.utils.exceptions import UserGraphCountExceededException, GraphVertexCountExceededException


def create_empty_graph(graph_name, user_id):
    if not validator.is_graph_count_exceed_by_user(user_id):
        raise UserGraphCountExceededException
    graph = Graph(graph_name, user_id)
    db_util.save_data_in_db(graph)
    return graph.id


def delete_graph(graph_id):
    graph_to_delete = db_util.get_data_from_db_or_404(Graph, graph_id)
    db_util.delete_data_in_db(graph_to_delete)


def update_graph_name(graph_id, new_graph_name):
    graph_to_update = db_util.get_data_from_db_or_404(Graph, graph_id)
    graph_to_update.name = new_graph_name
    db_util.save_data_in_db(graph_to_update)


def add_vertex_to_graph(graph_id, vertex_x, vertex_y):
    if not validator.is_graph_vertex_limit_exceed(graph_id):
        raise GraphVertexCountExceededException
    return vertex_service.create_vertex(x_position=vertex_x, y_position=vertex_y, graph_id=graph_id)


def update_vertex_position(vertex_id, new_x_position, new_y_position):
    vertex_service.update_vertex(vertex_id, new_x_position=new_x_position, new_y_position=new_y_position)


def delete_vertex_from_graph(graph_id, vertex_id):
    graph = db_util.get_data_from_db_or_404(Graph, graph_id)
    vertex_to_delete = db_util.get_data_from_db_or_404(Vertex, vertex_id)
    vertex_service.delete_all_neighbors(vertex_to_delete)
    _delete_vertex_with_incident_edges(graph, vertex_to_delete)
    vertex_service.delete_vertex(vertex_to_delete.id)


def add_edge_to_graph(graph_id, vertex_in_id, vertex_out_id):
    vertex_in = db_util.get_data_from_db_or_404(Vertex, vertex_in_id)
    vertex_out = db_util.get_data_from_db_or_404(Vertex, vertex_out_id)
    graph = db_util.get_data_from_db_or_404(Graph, graph_id)
    if _check_if_graph_has_edge(graph, vertex_in, vertex_out):
        return
    edge = edge_service.create_edge(vertex_in=vertex_in, vertex_out=vertex_out, graph_id=graph_id)
    vertex_service.add_neighbor_to_vertex(vertex_in, vertex_out)
    vertex_service.add_neighbor_to_vertex(vertex_out, vertex_in)
    return edge


def delete_edge_from_graph(edge_id):
    edge_to_delete = db_util.get_data_from_db_or_404(Edge, edge_id)
    vertex_in = edge_to_delete.vertex_in
    vertex_out = edge_to_delete.vertex_out
    vertex_service.delete_neighbor_from_vertex(vertex_in, vertex_out)
    vertex_service.delete_neighbor_from_vertex(vertex_out, vertex_in)
    edge_service.delete_edge(edge_id)


def get_graph_by_id(graph_id):
    graph = db_util.get_data_from_db_or_404(Graph, graph_id)
    vertices = graph.vertices.all()
    edges = graph.edges.all()
    return GraphDTO(id=graph_id, name=graph.name, vertices=vertices, edges=edges)


def _check_if_graph_has_edge(graph, vertex_in, vertex_out):
    edge = graph.edges.filter_by(vertex_in=vertex_in, vertex_out=vertex_out).first()
    return edge is not None


def _delete_vertex_with_incident_edges(graph, vertex):
    for edge in graph.edges.filter_by(vertex_in=vertex):
        edge_service.delete_edge(edge.id)
    for edge in graph.edges.filter_by(vertex_out=vertex):
        edge_service.delete_edge(edge.id)
