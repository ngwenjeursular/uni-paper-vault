""" 
initializing the flask app
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from datetime import datetime, timedelta
import os



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
print("Initializing app.")


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(Config)

    print("UPLOAD_FOLDER: ", Config.UPLOAD_FOLDER)

    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    

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
    #app.register_blueprint(user_bp)
    app.register_blueprint(user_bp, url_prefix='/user')

    with app.app_context():
        """Create the tables"""

        from app.models.user import User
        from app.models.comment import Comment
        from app.models.answer import Answer
        from app.models.upload import UploadedFile
        db.create_all()


    @app.template_filter('format_time')
    def format_time(dt):
        now = datetime.utcnow()
        diff = now - dt

        if diff < timedelta(minutes=1):
            return "just now"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff < timedelta(hours=24):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff < timedelta(days=1):
            return "yesterday"
        else:
            return dt.strftime("%a, %d %b %Y")  # Formats as 'Mon, 14 Oct 2024'

        # Register the filter in Jinja  
        app.jinja_env.filters['format_time'] = format_time

    import re

    def detect_mentions(content):
        # Simple regex for detecting @username
        mentions = re.findall(r'@(\w+)', content)
        return mentions


    return app  


