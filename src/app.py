from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import models
import views

db = SQLAlchemy()
admin = Admin()

admin.add_view(ModelView(models.clubmember, db.session))
admin.add_view(ModelView(models.location, db.session))
admin.add_view(views.clubmemberlocationView(models.clubmemberlocation, db.session))
# admin.add_view(ModelView(models.hobby, db.session))

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:toor@172.16.16.241:3306/mvc"
    app.config["SECRET_KEY"] = "MY_SECRET"

    db.init_app(app)
    admin.init_app(app)

    return app



# @app.route("/")
# def hello():
#     return "Hello, World!"