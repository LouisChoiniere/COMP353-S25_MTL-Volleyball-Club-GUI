from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# field_flags = {"requiredif": True}

class ClubMember(db.Model):
    __tablename__ = "clubmember"

    ClubMemberID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    DOB = db.Column(db.Date)
    Height = db.Column(db.Numeric(4, 1))
    Weight = db.Column(db.Numeric(4, 1))
    SSN = db.Column(db.String(9), unique=True)
    MedicareCardNumber = db.Column(db.String(20), unique=True)
    Phone = db.Column(db.String(20))
    Email = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    City = db.Column(db.String(100))
    Province = db.Column(db.String(100))
    PostalCode = db.Column(db.String(10))

    clubmemberlocations = db.relationship("ClubMemberLocation", back_populates="clubmember")
    hobbies = db.relationship('HasHobby', back_populates='clubmember')
    payments = db.relationship('Payment', back_populates='clubmember')

    def __str__(self):
        return self.FirstName + " " + self.LastName

class Location(db.Model):
    __tablename__ = "location"

    LocationID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Type = db.Column(db.Enum('Head', 'Branch'))
    Address = db.Column(db.String(255))
    City = db.Column(db.String(100))
    Province = db.Column(db.String(100))
    PostalCode = db.Column(db.String(10))
    Phone = db.Column(db.String(20))
    WebAddress = db.Column(db.String(100))
    Capacity = db.Column(db.Integer)

    clubmemberlocations = db.relationship("ClubMemberLocation", back_populates="location")

    def __str__(self):
        return self.Name + " [" + self.Type + "]"

class ClubMemberLocation(db.Model):
    __tablename__ = "clubmemberlocation"

    ClubMemberID = db.Column(db.ForeignKey("clubmember.ClubMemberID"), primary_key=True)
    LocationID = db.Column(db.ForeignKey("location.LocationID"), primary_key=True)
    StartDate = db.Column(db.Date, primary_key=True)
    EndDate = db.Column(db.Date)

    clubmember = db.relationship('ClubMember', back_populates='clubmemberlocations')
    location = db.relationship('Location', back_populates='clubmemberlocations')

    def __str__(self):
        return f"{self.location.Name}: {self.StartDate} to {self.EndDate}"

class Hobby(db.Model):
    __tablename__ = "hobby"

    HobbyName = db.Column(db.String(50), primary_key=True)

    hashobbies = db.relationship("HasHobby", back_populates="hobby")

    def __str__(self):
        return self.HobbyName

class HasHobby(db.Model):
    __tablename__ = "hashobby"

    ClubMemberID = db.Column(db.ForeignKey("clubmember.ClubMemberID"), primary_key=True)
    HobbyName = db.Column(db.ForeignKey("hobby.HobbyName"), primary_key=True)

    clubmember = db.relationship('ClubMember', back_populates='hobbies')
    hobby = db.relationship('Hobby', back_populates='hashobbies')

    def __str__(self):
        return f"{self.hobby}"

class Payment(db.Model):
    __tablename__ = "payment"

    PaymentID = db.Column(db.Integer, primary_key=True)
    ClubMemberID = db.Column(db.ForeignKey("clubmember.ClubMemberID"))
    Amount = db.Column(db.Numeric(10, 2))
    PaymentDate = db.Column(db.Date)
    MembershipYear = db.Column(db.Integer)
    Method = db.Column(db.Enum('Cash', 'Debit', 'Credit'))
    InstallmentNo = db.Column(db.Integer)

    clubmember = db.relationship('ClubMember', back_populates='payments')

    __table_args__ = (
        db.CheckConstraint('InstallmentNo BETWEEN 1 AND 4', name='Payment_chk_1'),
    )