from app.models import Vertex
from app.utils import database_util as db


def save_vertex(x_position, y_position):
    vertex = Vertex(x=x_position, y=y_position)
    db.save_data_in_db(vertex)


def delete_vertex(vertex_id):
    vertex_to_delete = Vertex.query.get_or_404(vertex_id)
    db.delete_data_in_db(vertex_to_delete)


def update_vertex(vertex_id, new_x_position, new_y_position):
    vertex_to_update = Vertex.query.get_or_404(vertex_id)
    vertex_to_update.x = new_x_position
    vertex_to_update.y = new_y_position
    db.save_data_in_db(vertex_to_update)
