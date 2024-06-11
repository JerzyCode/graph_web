from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(db_url='sqlite:///app.db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SECRET_KEY'] = 'nosecretkeeycurrently'
    app.template_folder = '../templates/'
    app.static_folder = '../static/'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

    from app.controllers.main_controller import main_bp
    app.register_blueprint(main_bp)

    from app.controllers.graph_controller import graph_bp
    app.register_blueprint(graph_bp)

    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    return app
