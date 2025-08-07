from flask_admin.contrib.sqla import ModelView

class clubmemberView(ModelView):
    form_columns = ["FirstName", "LastName", "DOB", "Height", "Weight", "SSN", "MedicareCardNumber", "Phone", "Email", "Address", "City", "Province", "PostalCode"]
    list_columns = ["FirstName", "LastName", "DOB", "Height", "Weight", "SSN", "MedicareCardNumber", "Phone", "Email", "Address", "City", "Province", "PostalCode", "clubmemberlocations", "hobbies"]

class locationView(ModelView):
    form_columns = ["Name","Type","Address","City","Province","PostalCode","Phone","WebAddress","Capacity"]
    list_columns = ["Name","Type","Address","City","Province","PostalCode","Phone","WebAddress","Capacity"]

class clubmemberlocationView(ModelView):
    form_columns = ["clubmember", "location", "StartDate", "EndDate"]
    list_columns = ["clubmember", "location", "StartDate", "EndDate"]

class hobbyView(ModelView):
    form_columns = ["HobbyName"]
    list_columns = ["HobbyName"]

class hashobbyView(ModelView):
    form_columns = ["clubmember", "hobby"]
    list_columns = ["clubmember", "hobby"]

class operatesatView(ModelView):
    form_columns = ["personnel", "location", "StartDate", "EndDate"]
    list_columns = ["personnel", "location", "StartDate", "EndDate"]

class isrelatedto(ModelView):
    form_columns = ["clubmember", "familymember", "RelationshipType"]
    list_columns = ["clubmember", "familymember", "RelationshipType"]