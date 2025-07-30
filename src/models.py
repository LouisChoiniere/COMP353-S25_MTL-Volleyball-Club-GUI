from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

field_flags = {"requiredif": True}

class clubmember(db.Model):
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

    clubmemberlocation = db.relationship("clubmemberlocation", back_populates="clubmember")

    def __str__(self):
        return self.FirstName + " " + self.LastName

class location(db.Model):
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

    clubmemberlocation = db.relationship("clubmemberlocation", back_populates="location")

    def __str__(self):
        return self.Name + " [" + self.Type + "]"

class clubmemberlocation(db.Model):
    ClubMemberID = db.Column(db.ForeignKey("clubmember.ClubMemberID"), primary_key=True)
    LocationID = db.Column(db.ForeignKey("location.LocationID"), primary_key=True)
    StartDate = db.Column(db.Date, primary_key=True)
    EndDate = db.Column(db.Date)

    clubmember = db.relationship('clubmember', back_populates='clubmemberlocation')
    location = db.relationship('location', back_populates='clubmemberlocation')

class hobby(db.Model):
    HobbyName = db.Column(db.String(50), primary_key=True)
