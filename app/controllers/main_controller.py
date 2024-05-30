from flask import render_template, Blueprint

from app.models import Vertex

main_bp = Blueprint('index', __name__, url_prefix='/')


@main_bp.route('/')
def index():
    vertices = Vertex.query.all()
    print(vertices)
    return render_template('index.html', vertices=vertices)
