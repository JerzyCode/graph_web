from flask import Blueprint, request, jsonify

from app.services import graph_service

graph_bp = Blueprint('graph', __name__, url_prefix='/graph/')


class GraphController:
    def __init__(self, service):
        self._service = service

    def handle_create_graph_request(self, req):
        graph_name = req.args.get('graph_name')
        if graph_name is None:
            return 'No graph name provided', 400
        else:
            self._service.create_empty_graph(graph_name=graph_name)
            return 'Graph created successfully', 200

    def handle_delete_graph_request(self, req):
        graph_id = req.args.get('graph_id')
        if graph_id is None:
            return 'No graph_id provided', 400
        else:
            self._service.delete_graph(graph_id=graph_id)
            return "Graph successfully deleted", 200

    def handle_get_graph_request(self, req):
        graph_id = req.args.get('graph_id')
        if graph_id is None:
            return 'No graph_id provided', 400
        else:
            graph_dto = self._service.get_graph_by_id(graph_id=graph_id)
            return jsonify(graph_dto.map_to_dictionary()), 200

    def handle_create_vertex_request(self, req):
        graph_id = req.args.get('graph_id')
        vertex_x = req.args.get('x')
        vertex_y = req.args.get('y')
        if graph_id is None or vertex_x is None or vertex_y is None:
            return 'No graph_id, x or y provided', 400
        else:
            self._service.add_vertex_to_graph(graph_id=graph_id, vertex_x=vertex_x, vertex_y=vertex_y)
            return 'Added vertex', 200

    def handle_delete_vertex_request(self, req):
        graph_id = req.args.get('graph_id')
        vertex_id = req.args.get('vertex_id')
        if graph_id is None:
            return 'No graph_id or vertex_id provided', 400
        else:
            self._service.delete_vertex_from_graph(graph_id=graph_id, vertex_id=vertex_id)
            return 'Deleted vertex', 200

    def handle_create_edge_request(self, req):
        graph_id = req.args.get('graph_id')
        vertex_in_id = req.args.get('vertex_in_id')
        vertex_out_id = req.args.get('vertex_out_id')
        if graph_id is None or vertex_in_id is None or vertex_out_id is None:
            return 'No graph_id, vertex_out_id vertex_in_id y provided', 400
        else:
            self._service.add_edge_to_graph(graph_id=graph_id, vertex_in_id=vertex_in_id, vertex_out_id=vertex_out_id)
            return 'Added edge', 200

    def handle_delete_edge_request(self, req):
        edge_id = req.args.get('edge_id')
        if edge_id is None:
            return 'No edge_id provided', 400
        else:
            self._service.delete_edge_from_graph(edge_id=edge_id)
            return 'Deleted edge', 200


graph_controller: GraphController = GraphController(service=graph_service)


@graph_bp.route(rule='/', methods=['POST', 'DELETE', 'GET'])
def graph_endpoints():
    if request.method == 'POST':
        return graph_controller.handle_create_graph_request(request)
    elif request.method == 'DELETE':
        return graph_controller.handle_delete_graph_request(request)
    elif request.method == 'GET':
        return graph_controller.handle_get_graph_request(request)
    # TODO UPDATE_NAME


@graph_bp.route(rule='/vertex', methods=['POST', 'DELETE'])
def vertex_endpoints():
    if request.method == 'POST':
        return graph_controller.handle_create_vertex_request(request)
    elif request.method == 'DELETE':
        return graph_controller.handle_delete_vertex_request(request)
    # TODO add update x and y for vertex


@graph_bp.route(rule='/edge', methods=['POST', 'DELETE'])
def edge_endpoints():
    if request.method == 'POST':
        return graph_controller.handle_create_edge_request(request)
    elif request.method == 'DELETE':
        return graph_controller.handle_delete_edge_request(request)
