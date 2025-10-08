from flask import Flask 
from .config import Config
from .routes.auth import user_bp
from .routes.mangement import manage_bp
from .extensions import jwt,db

def create_app():
    app=Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(manage_bp)

    with app.app_context():
        db.create_all()

    return app 
