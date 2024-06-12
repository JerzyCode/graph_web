from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user

from app.app import db
from app.models import Graph
from app.services import graph_service
from app.utils.exceptions import UserGraphCountExceededException
from app.utils.request_validator import validate_request

graph_bp = Blueprint('graph', __name__, url_prefix='/graph/')


class GraphController:
    def __init__(self, service):
        self._service = service

    def handle_create_graph_request(self, req):
        graph_name = req.args.get('graph_name')
        if graph_name is None:
            return 'No graph name provided', 400
        else:
            user_id = current_user.id
            try:
                graph_id = self._service.create_empty_graph(graph_name=graph_name, user_id=user_id)
            except UserGraphCountExceededException as ex:
                return {'error': ex.message}, 400
            return {'graph_id': graph_id}, 200

    def handle_delete_graph_request(self, req):
        graph_id = req.args.get('graph_id')
        self._service.delete_graph(graph_id=graph_id)
        return "Graph successfully deleted", 200

    def handle_get_graph_request(self, req):
        graph_id = req.args.get('graph_id')
        graph_dto = self._service.get_graph_by_id(graph_id=graph_id)
        return jsonify(graph_dto.map_to_dictionary()), 200

    def handle_put_graph_request(self, req):
        graph_id = req.args.get('graph_id')
        new_name = req.args.get('name')
        if new_name is None:
            return 'No name provided', 400
        else:
            self._service.update_graph_name(graph_id=graph_id, new_graph_name=new_name)
            return 'Updated graph name', 200

    def handle_create_vertex_request(self, req):
        graph_id = req.args.get('graph_id')
        vertex_x = req.args.get('x')
        vertex_y = req.args.get('y')
        if vertex_x is None or vertex_y is None:
            return 'No x or y provided', 400
        else:
            created_vertex = self._service.add_vertex_to_graph(graph_id=graph_id, vertex_x=vertex_x, vertex_y=vertex_y)
            return jsonify(created_vertex.to_dict()), 200

    def handle_delete_vertex_request(self, req):
        graph_id = req.args.get('graph_id')
        vertex_id = req.args.get('vertex_id')
        if vertex_id is None:
            return 'No vertex_id provided', 400
        else:
            self._service.delete_vertex_from_graph(graph_id=graph_id, vertex_id=vertex_id)
            return 'Deleted vertex', 200

    def handle_put_vertex_request(self, req):
        vertex_id = req.args.get('vertex_id')
        new_x_position = req.args.get('x')
        new_y_position = req.args.get('y')
        if vertex_id is None or new_x_position is None or new_y_position is None:
            return 'No vertex_id, x or y provided', 400
        else:
            self._service.update_vertex_position(vertex_id=vertex_id, new_x_position=new_x_position, new_y_position=new_y_position)
            return 'Updated vertex', 200

    def handle_create_edge_request(self, req):
        graph_id = req.args.get('graph_id')
        vertex_in_id = req.args.get('vertex_in_id')
        vertex_out_id = req.args.get('vertex_out_id')
        if vertex_in_id is None or vertex_out_id is None:
            return 'No graph_id, vertex_out_id vertex_in_id y provided', 400
        else:
            created_edge = self._service.add_edge_to_graph(graph_id=graph_id, vertex_in_id=vertex_in_id, vertex_out_id=vertex_out_id)
            return jsonify(created_edge.to_dict()), 200

    def handle_delete_edge_request(self, req):
        edge_id = req.args.get('edge_id')
        if edge_id is None:
            return 'No edge_id provided', 400
        else:
            self._service.delete_edge_from_graph(edge_id=edge_id)
            return 'Deleted edge', 200


graph_controller: GraphController = GraphController(service=graph_service)


@graph_bp.route(rule='/', methods=['DELETE', 'GET', 'PUT'])
@login_required
@validate_request
def graph_endpoints():
    if request.method == 'DELETE':
        return graph_controller.handle_delete_graph_request(request)
    elif request.method == 'GET':
        return graph_controller.handle_get_graph_request(request)
    elif request.method == 'PUT':
        return graph_controller.handle_put_graph_request(request)


@graph_bp.route(rule='/', methods=['POST'])
@login_required
def post_graph_endpoint():
    if request.method == 'POST':
        return graph_controller.handle_create_graph_request(request)


@graph_bp.route(rule='/vertex', methods=['POST', 'DELETE', 'PUT'])
@login_required
@validate_request
def vertex_endpoints():
    if request.method == 'POST':
        return graph_controller.handle_create_vertex_request(request)
    elif request.method == 'DELETE':
        return graph_controller.handle_delete_vertex_request(request)
    elif request.method == 'PUT':
        return graph_controller.handle_put_vertex_request(request)


@graph_bp.route(rule='/edge', methods=['POST', 'DELETE'])
@login_required
@validate_request
def edge_endpoints():
    if request.method == 'POST':
        return graph_controller.handle_create_edge_request(request)
    elif request.method == 'DELETE':
        return graph_controller.handle_delete_edge_request(request)


@graph_bp.route('/getAllGraphs')
def render_graphs_popup():
    user_id = current_user.id
    graphs = db.session.query(Graph).filter_by(user_id=user_id).all()
    graphs_data = [{'id': graph.id, 'name': graph.name} for graph in graphs]
    return render_template('load_graph_popup.html', graphs=graphs_data)
