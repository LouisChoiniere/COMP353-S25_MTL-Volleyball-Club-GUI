from flask import Flask, render_template
from sqlalchemy import text

def init_routes(app, db):
    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/makepayment")
    def make_payment():
        return render_template('makepayment.html')

    @app.route("/listlocations")
    def list_locations():
        
        locations = db.session.query(
            db.column('Name'),
            db.column('Address'),
            db.column('city'),
            db.column('Province'),
            db.column('PostalCode'),
            db.column('Phone'),
            db.column('WebAddress'),
            db.column('Type'),
            db.column('Capacity'),
            db.column('GeneralManagerName'),
            db.column('MinorClubMembersCount'),
            db.column('MajorClubMembersCount'),
            db.column('TeamCount'),
        ).from_statement(text("""
SELECT
    `Name`,
    `Address`,
    `city`,
    `Province`,
    `PostalCode`,
    `Phone`,
    `WebAddress`,
    `Type`,
    `Capacity`,
    '' as `GeneralManagerName`,
    0 AS `MinorClubMembersCount`,
    0 AS `MajorClubMembersCount`,
    0 AS `TeamCount`
FROM 
    `location` as l
ORDER BY 
    `province` ASC,
    `city` ASC;
"""))

        return render_template('listlocation.html', locations=locations)