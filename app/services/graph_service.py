from app.models import Graph
from app.services import vertex_service
from app.utils import database_util as db_util


def create_empty_graph(graph_name):
    graph = Graph(graph_name)
    db_util.save_data_in_db(graph)


def delete_graph(graph_id):
    graph_to_delete = Graph.query.get_or_404(graph_id)
    db_util.delete_data_in_db(graph_to_delete)


def add_vertex_to_graph(graph_id, vertex_x, vertex_y):
    vertex_service.create_vertex(x_position=vertex_x, y_position=vertex_y, graph_id=graph_id)
