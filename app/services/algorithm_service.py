from app.models import Graph
from app.utils import algorithms as alg
from app.utils import database_util as db_util, mapper
from app.utils.classes import GraphAlgorithm


def prepare_graph(graph_id) -> GraphAlgorithm:
    graph = db_util.get_data_from_db_or_404(Graph, graph_id)
    prepared_graph = mapper.algorithm_graph_of_model_graph(graph)
    return prepared_graph


def run_dfs_algorithm(graph_id):
    graph = prepare_graph(graph_id)
    objects_to_color = alg.depth_search(graph)
    return objects_to_color
