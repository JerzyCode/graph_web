from flask import render_template, Blueprint

from app.app import db
from app.models import Graph

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/home')
def home():
    return render_template('home.html')


@main_bp.route('/getAllGraphs')
def render_graphs_popup():
    graphs = db.session.query(Graph).all()
    graphs_data = [{'id': graph.id, 'name': graph.name} for graph in graphs]
    return render_template('load_graph_popup.html', graphs=graphs_data)


@main_bp.route('/')
def main_page():
    return render_template('index.html')
