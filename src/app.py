from flask import Flask, render_template

from init_flask_admin import init_flask_admin
from init_error_handlers import init_error_handlers
from init_db import init_db
from init_routes import init_routes


def create_app():
    app = Flask(__name__)
    
    db = init_db(app)
    init_error_handlers(app)
    admin = init_flask_admin(app, db)

    init_routes(app, db)

    return app