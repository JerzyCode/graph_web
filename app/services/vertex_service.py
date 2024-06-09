from app.models import Vertex
from app.utils import database_util as db_util


def create_vertex(x_position, y_position, graph_id=None):
    vertex = Vertex(x=x_position, y=y_position, graph_id=graph_id)
    db_util.save_data_in_db(vertex)
    return vertex


def delete_vertex(vertex_id):
    vertex_to_delete = db_util.get_data_from_db_or_404(Vertex, vertex_id)
    db_util.delete_data_in_db(vertex_to_delete)


def update_vertex(vertex_id, new_x_position, new_y_position):
    vertex_to_update = db_util.get_data_from_db_or_404(Vertex, vertex_id)
    vertex_to_update.x = new_x_position
    vertex_to_update.y = new_y_position
    db_util.save_data_in_db(vertex_to_update)


# adding only in one way
def add_neighbor_to_vertex(vertex, neighbor):
    vertex.neighbors.append(neighbor)
    db_util.save_data_in_db(vertex)


# removing only in one way
def delete_neighbor_from_vertex(vertex, neighbor):
    vertex.neighbors.remove(neighbor)
    db_util.save_data_in_db(vertex)


def delete_all_neighbors(vertex):
    neighbors_copy = list(vertex.neighbors)
    for neighbor in neighbors_copy:
        delete_neighbor_from_vertex(vertex, neighbor)
