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