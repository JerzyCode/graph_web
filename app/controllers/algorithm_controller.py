from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.services import algorithm_service

algorithm_bp = Blueprint('algorithm', __name__, url_prefix='/algorithm/')


@algorithm_bp.route('/dfs', methods=['GET'])
@login_required
def dfs_endpoint():
    graph_id = request.args.get('graph_id')
    if graph_id is None:
        return 'No graph_id provided', 400
    objects_to_color = algorithm_service.run_dfs_algorithm(graph_id)
    objects_dict = [obj.to_dict() for obj in objects_to_color]
    return jsonify(objects_dict), 200
