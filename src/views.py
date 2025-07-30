from flask_admin.contrib.sqla import ModelView

class clubmemberlocationView(ModelView):
    form_columns = ["clubmember", "location", "StartDate", "EndDate"]
    list_columns = ["clubmember", "location", "StartDate", "EndDate"]