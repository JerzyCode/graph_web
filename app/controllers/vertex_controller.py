from flask import request, Blueprint, jsonify, make_response

from app.app import db
from app.models import Vertex
from app.services import vertex_service as vertex_service

vertex_bp = Blueprint('main', __name__, url_prefix='/vertex')


@vertex_bp.route(rule='', methods=['POST'])
def add_vertex():
    x = request.args.get('x')
    y = request.args.get('y')
    vertex_service.create_vertex(x, y)
    response = make_response('Vertex added successfully', 200)
    return response


@vertex_bp.route(rule='', methods=['GET'])
def get_all_vertices():
    vertices = Vertex.query.all()
    vertices_json = [vertex.to_dict() for vertex in vertices]
    return jsonify(vertices_json)


@vertex_bp.route(rule='', methods=['DELETE'])
def delete_vertex():
    vertex_id = request.args.get('id')
    vertex_to_delete = Vertex.query.get_or_404(vertex_id)
    db.session.delete(vertex_to_delete)
    db.session.commit()
    return "Vertex deleted successfully"


@vertex_bp.route(rule='', methods=['PUT'])
def update_vertex():
    vertex_id = request.args.get('id')
    new_x = request.args.get('x')
    new_y = request.args.get('y')
    vertex_to_update = Vertex.query.get_or_404(vertex_id)
    vertex_to_update.x = new_x
    vertex_to_update.y = new_y
    db.session.add(vertex_to_update)
    db.session.commit()
    return "Vertex updated successfully"
