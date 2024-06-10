from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app.app import db
from app.models import Graph

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/home')
def welcome_page():
    return render_template('home.html')


@main_bp.route('/getAllGraphs')
def render_graphs_popup():
    graphs = db.session.query(Graph).all()
    graphs_data = [{'id': graph.id, 'name': graph.name} for graph in graphs]
    return render_template('load_graph_popup.html', graphs=graphs_data)


@main_bp.route('/')
@login_required
def main_graph_panel():
    print(current_user)
    return render_template('index.html')
