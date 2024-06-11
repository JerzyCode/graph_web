from flask import render_template, Blueprint
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/home')
def welcome_page():
    return render_template('home.html')


@main_bp.route('/graph_panel')
@login_required
def main_graph_panel():
    print(current_user)
    return render_template('graph_panel.html')
