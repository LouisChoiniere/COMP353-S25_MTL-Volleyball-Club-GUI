from flask import render_template
from sqlalchemy import text

def init_routes_reports(app, db):

    @app.route("/reports/11")
    def report_11():
        
        clubmembers = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName
            FROM
                clubmember AS cm
                JOIN clubmemberlocation AS cml ON cm.ClubMemberID = cml.ClubMemberID
            WHERE
                cm.Status = 'Inactive'
                AND DATEDIFF(CURDATE(), cm.DateJoined) >= 730 -- 730 days = 2 years
            GROUP BY
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName
            HAVING
                COUNT(cml.LocationID) >= 2
            ORDER BY
                cm.ClubMemberID ASC;
        """))

        return render_template('reports/11.html', data=clubmembers)
    
    @app.route("/reports/13")
    def report_13():
        
        clubmembers = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName'),
            db.column('Age'),
            db.column('Phone'),
            db.column('Email'),
            db.column('CurrentLocationNames')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                TIMESTAMPDIFF(YEAR, cm.DOB, CURDATE()) AS Age,
                cm.Phone,
                cm.Email,
                GROUP_CONCAT(
                    l.Name
                    ORDER BY
                        l.Name ASC SEPARATOR ', '
                ) AS CurrentLocationNames
            FROM
                ClubMember cm
                LEFT JOIN PlaysIn PI ON cm.ClubMemberID = PI.ClubMemberID
                LEFT JOIN ClubMemberLocation cml ON cm.ClubMemberID = cml.ClubMemberID
                AND cml.EndDate IS NULL
                LEFT JOIN Location l ON cml.LocationID = l.LocationID
            WHERE
                cm.Status = 'Active'
                AND PI.FormationID IS NULL
            GROUP BY
                cm.ClubMemberID
            ORDER BY
                CurrentLocationNames,
                Age;
        """))

        return render_template('reports/13.html', data=clubmembers)
    
    @app.route("/reports/14")
    def report_14():
        
        clubmembers = db.session.query(
            db.column('ClubMemberID'),
            db.column('FirstName'),
            db.column('LastName'),
            db.column('DateJoined'),
            db.column('Age'),
            db.column('Phone'),
            db.column('Email'),
            db.column('CurrentLocationNames')
        ).from_statement(text("""
            SELECT
                cm.ClubMemberID,
                cm.FirstName,
                cm.LastName,
                cm.DateJoined,
                TIMESTAMPDIFF(YEAR, cm.DOB, cm.DateJoined) AS Age,
                cm.Phone,
                cm.Email,
                GROUP_CONCAT(
                    l.Name
                    ORDER BY
                        l.Name ASC SEPARATOR ', '
                ) AS CurrentLocationNames
            FROM
                ClubMember cm
                LEFT JOIN ClubMemberLocation cml ON cm.ClubMemberID = cml.ClubMemberID
                AND (
                    cml.EndDate IS NULL
                    OR cml.EndDate < CURDATE()
                )
                LEFT JOIN Location l ON cml.LocationID = l.LocationID
            WHERE
                cm.Status LIKE "Active"
                AND TIMESTAMPDIFF(YEAR, cm.DOB, cm.DateJoined) < 18
                AND cm.`Type` LIKE "Major"
            GROUP BY
                cm.ClubMemberID
            ORDER BY
                CurrentLocationNames ASC,
                Age ASC;
        """))

        return render_template('reports/14.html', data=clubmembers)