from app.models import Edge
from app.utils import database_util as db_util


def create_edge(vertex_in, vertex_out, graph_id=None):
    edge = Edge(vertex_in, vertex_out, graph_id=graph_id)
    db_util.save_data_in_db(edge)


def delete_edge(edge_id):
    edge = Edge.query.get_or_404(edge_id)
    db_util.delete_data_in_db(edge)


def is_vertex_in_edge(vertex, edge):
    return edge.vertex_in == vertex or edge.vertex_out == vertex
