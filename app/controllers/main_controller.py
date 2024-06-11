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
    user_id = current_user.id
    graphs = db.session.query(Graph).filter_by(user_id=user_id).all()
    graphs_data = [{'id': graph.id, 'name': graph.name} for graph in graphs]
    return render_template('load_graph_popup.html', graphs=graphs_data)


@main_bp.route('/graph_panel')
@login_required
def main_graph_panel():
    print(current_user)
    return render_template('graph_panel.html')
