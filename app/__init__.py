from datetime import timedelta
import os
from flask import Flask

from app.config import db
from app.routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'tooltrack.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    
    db.init_app(app)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_routes(app)

    with app.app_context():

        db.create_all()

    return app