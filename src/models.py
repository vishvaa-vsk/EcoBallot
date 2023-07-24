from .extensions import db

class Students(db.Model):
    rollNo = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    splVotes = db.relationship('SplTable',backref='students')
    asplSrSecVotes = db.relationship('Aspl_Sr_Sec_Table',backref='students',cascade="all, delete-orphan")
    asplHSecVotes = db.relationship('Aspl_hSec_Table',backref='students',cascade="all, delete-orphan")
    asplMiddleVotes = db.relationship('Aspl_Middle_Table',backref='students',cascade="all, delete-orphan")

class SplTable(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    splVotes = db.Column(db.String(50),nullable=False)

class Aspl_Sr_Sec_Table(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    asplVotes = db.Column(db.String(50),nullable=False)

class Aspl_hSec_Table(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    asplVotes = db.Column(db.String(50),nullable=False)

class Aspl_Middle_Table(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    asplVotes = db.Column(db.String(50),nullable=False)

class AdminTable(db.Model):
    _id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    passwd = db.Column(db.String(500),nullable=False)

class CandidateDetails(db.Model):
    _id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    position = db.Column(db.String(100),nullable=False)
    imageName = db.Column(db.String(500),nullable=False)
    