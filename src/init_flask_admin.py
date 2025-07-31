from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import models
import views

def init_flask_admin(app, db):
    admin = Admin()

    admin.add_view(views.clubmemberView(models.ClubMember, db.session))
    admin.add_view(views.locationView(models.Location, db.session))
    admin.add_view(views.clubmemberlocationView(models.ClubMemberLocation, db.session))
    admin.add_view(views.hobbyView(models.Hobby, db.session))
    admin.add_view(views.hashobbyView(models.HasHobby, db.session))
    admin.add_view(ModelView(models.Payment, db.session))

    admin.init_app(app)

    return admin