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

class TeamFormation(db.Model):
    __tablename__ = "teamformation"

    FormationID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    StartTime = db.Column(db.Time)
    Address = db.Column(db.String(255))
    SessionType = db.Column(db.Enum('Training', 'Game'))
    ScoreTeamA = db.Column(db.Integer)
    ScoreTeamB = db.Column(db.Integer)

    playsin = db.relationship('PlaysIn', back_populates='teamformation')

    def __str__(self):
        return f"Formation {self.FormationID}: {self.Date} {self.StartTime} - {self.SessionType}"

class PlaysIn(db.Model):
    __tablename__ = "playsin"

    FormationID = db.Column(db.ForeignKey("teamformation.FormationID"), primary_key=True)
    ClubMemberID = db.Column(db.ForeignKey("clubmember.ClubMemberID"), primary_key=True)
    RoleInTeam = db.Column(db.Enum('Setter','OutsideHitter','OppositeHitter','MiddleBlocker','DefensiveSpecialist','Libero'))

    teamformation = db.relationship('TeamFormation', back_populates='playsin')
    clubmember = db.relationship('ClubMember')

    def __str__(self):
        return f"ClubMember {self.ClubMemberID} in Formation {self.FormationID} as {self.RoleInTeam}"
    
class Personnel(db.Model):
    __tablename__ = "personnel"

    PersonnelID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    DOB = db.Column(db.Date)
    SSN = db.Column(db.String(9), unique=True, nullable=False)
    MedicareCardNumber = db.Column(db.String(20), unique=True)
    Phone = db.Column(db.String(20))
    Email = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    City = db.Column(db.String(100))
    Province = db.Column(db.String(100))
    PostalCode = db.Column(db.String(10))
    Role = db.Column(db.Enum('Administrator','Coach','HeadCoach','Other'))
    Mandate = db.Column(db.Enum('Volunteer','Salaried'))

    def __str__(self):
        return f"{self.FirstName} {self.LastName} ({self.Role}, {self.Mandate})"
    
class OperatesAt(db.Model):
    __tablename__ = "operatesat"

    PersonnelID = db.Column(db.ForeignKey("personnel.PersonnelID"), primary_key=True)
    LocationID = db.Column(db.ForeignKey("location.LocationID"), primary_key=True)
    StartDate = db.Column(db.Date, primary_key=True)
    EndDate = db.Column(db.Date)

    personnel = db.relationship('Personnel')
    location = db.relationship('Location')

    def __str__(self):
        return f"Personnel {self.PersonnelID} at Location {self.LocationID}: {self.StartDate} to {self.EndDate}"


class FamilyMember(db.Model):
    __tablename__ = "familymember"

    FamilySSN = db.Column(db.String(9), primary_key=True, nullable=False)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    DOB = db.Column(db.Date)
    MedicareCardNumber = db.Column(db.String(20), unique=True)
    Phone = db.Column(db.String(20))
    Email = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    City = db.Column(db.String(100))
    Province = db.Column(db.String(100))
    PostalCode = db.Column(db.String(10))

    def __str__(self):
        return f"{self.FirstName} {self.LastName} (SSN: {self.FamilySSN})"
    
class IsRelatedTo(db.Model):
    __tablename__ = "isrelatedto"

    ClubMemberID = db.Column(db.ForeignKey("clubmember.ClubMemberID"), primary_key=True)
    FamilySSN = db.Column(db.ForeignKey("familymember.FamilySSN"), primary_key=True)
    RelationshipType = db.Column(db.String(50))

    clubmember = db.relationship('ClubMember')
    familymember = db.relationship('FamilyMember')

    def __str__(self):
        return f"ClubMember {self.ClubMemberID} is related to FamilyMember {self.FamilySSN} as {self.RelationshipType}"
