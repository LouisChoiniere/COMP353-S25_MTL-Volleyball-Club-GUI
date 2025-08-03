from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import text

def init_routes(app, db):
    @app.route("/")
    def index():
        return render_template('index.html')
    
    @app.route("/makepayment")
    def make_payment():
        return render_template('makepayment.html')
    
    @app.route("/submit-payment", methods=['POST'])
    def submit_payment():
        member_number = request.form['memberNumber']
        amount = request.form['amount']
        payment_date = request.form['paymentDate']
        payment_method = request.form['paymentMethod']
        payment_method = request.form['instalement']

        db.session.execute(text("""
            INSERT INTO payment (ClubMemberID, Amount, PaymentDate, MembershipYear, Method, InstallmentNo)
            VALUES (:memberNumber, :amount, :paymentDate, :membershipYear, :paymentMethod, :instalement)
        """), {
            'memberNumber': member_number,
            'amount': amount,
            'paymentDate': payment_date,
            'membershipYear': int(payment_date[:4]) + 1,
            'paymentMethod': payment_method,
            'instalement': payment_method
        })
        db.session.commit()

        print(member_number)

        return redirect(url_for('index'))

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
                l.Name,
                l.Address,
                l.city,
                l.Province,
                l.PostalCode,
                l.Phone,
                l.WebAddress,
                l.Type,
                l.Capacity,
                CONCAT(p.FirstName, ' ', p.LastName) AS GeneralManagerName,
                SUM(CASE WHEN cm.Type = 'Minor' THEN 1 ELSE 0 END) AS MinorClubMembersCount,
                SUM(CASE WHEN cm.Type = 'Major' THEN 1 ELSE 0 END) AS MajorClubMembersCount,
                COUNT(DISTINCT t.TeamID) AS TeamCount
            FROM
                location AS l
                LEFT JOIN operatesat AS op ON op.LocationID = l.LocationID
                    AND (op.EndDate IS NULL OR op.EndDate < CURDATE())
                LEFT JOIN personnel AS p ON p.PersonnelID = op.PersonnelID
                    AND p.Role = 'Administrator'
                LEFT JOIN clubmemberlocation AS cml ON cml.LocationID = l.LocationID
                    AND (cml.EndDate IS NULL OR cml.EndDate < CURDATE())
                LEFT JOIN clubmember cm ON cm.ClubMemberID = cml.ClubMemberID
                LEFT JOIN team t ON t.LocationID = l.LocationID
            GROUP BY
                l.LocationID,
                l.Name,
                l.Address,
                l.city,
                l.Province,
                l.PostalCode,
                l.Phone,
                l.WebAddress,
                l.Type,
                l.Capacity,
                p.FirstName,
                p.LastName
            ORDER BY
                l.Province ASC,
                l.city ASC;
        """))

        return render_template('listlocation.html', locations=locations)
    
    @app.route("/reports")
    def reports():
        return render_template('reports.html')