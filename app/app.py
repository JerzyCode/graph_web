from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.template_folder = '../templates/'
    app.static_folder = '../static/'
    db.init_app(app)
    from app.controllers.main_controller import main_bp
    from app.controllers.vertex_controller import vertex_bp
    app.register_blueprint(vertex_bp)
    app.register_blueprint(main_bp)
    return app
