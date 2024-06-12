from app.models import User, Graph
from app.utils import database_util as db_util
from app.utils.constants import MAX_GRAPHS_PER_USER, MAX_VERTICES_PER_GRAPH


def is_graph_count_exceed_by_user(user_id):
    user = db_util.get_data_from_db_or_404(User, user_id)
    return user.graphs.count() <= MAX_GRAPHS_PER_USER


def is_graph_vertex_limit_exceed(graph_id):
    graph = db_util.get_data_from_db_or_404(Graph, graph_id)
    return graph.vertices.count() <= MAX_VERTICES_PER_GRAPH
