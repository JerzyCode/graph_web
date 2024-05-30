from app.models import Edge
from app.utils import database_util as db_util


def create_edge(vertex_in, vertex_out):
    edge = Edge(vertex_in, vertex_out)
    db_util.save_data_in_db(edge)


def delete_edge(edge_id):
    edge = Edge.query.get_or_404(edge_id)
    db_util.delete_data_in_db(edge)
