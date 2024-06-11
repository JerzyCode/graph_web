from functools import wraps

from flask import request, abort
from flask_login import current_user

from app.models import Graph
from app.utils.database_util import get_data_from_db_or_404


def validate_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('request validator')
        graph_id = request.args.get('graph_id')
        check_if_graph_id_exists(graph_id)

        graph = get_data_from_db_or_404(Graph, graph_id)
        check_if_graph_belongs_to_current_user(graph)

        return f(*args, **kwargs)

    return decorated_function


def check_if_graph_id_exists(graph_id):
    print('check_if_graph_id_exists(), graph_id=' + str(graph_id))
    if graph_id is None:
        abort(400, description="Graph ID is required.")


def check_if_graph_belongs_to_current_user(graph):
    user_id = current_user.id
    print('check_if_graph_belongs_to_user() userId=' + str(user_id))
    if graph.user_id != user_id:
        abort(400, description="You are not owner of graph!.")
