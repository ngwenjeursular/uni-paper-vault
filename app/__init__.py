""" 
initializing the flask app
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    """import the blueprints"""
    from app.routes.home import home_bp
    from app.routes.question import question_bp
    from app.routes.user import user_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        """Create the tables"""
        db.create_all()

    return app  