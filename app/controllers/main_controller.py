from flask import render_template, Blueprint

from app.app import db
from app.models import Vertex, Graph

main_bp = Blueprint('index', __name__, url_prefix='/')


@main_bp.route('/')
def index():
    vertices = Vertex.query.all()
    print(vertices)
    return render_template('index.html', vertices=vertices)


@main_bp.route('/getAllGraphs')
def render_graphs_popup():
    graphs = db.session.query(Graph).all()
    graphs_data = [{'id': graph.id, 'name': graph.name} for graph in graphs]
    return render_template('load_graph_popup.html', graphs=graphs_data)
