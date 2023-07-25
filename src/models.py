# The line `from .extensions import db` is importing the `db` object from the `extensions` module in
# the current package or directory. This `db` object is likely an instance of a database connection or
# ORM (Object-Relational Mapping) tool, such as SQLAlchemy, which is used to interact with the
# database in the application.
from .extensions import db

# The Students class represents a table in a database with columns for rollNo, name, and relationships
# to other tables for special votes, senior secondary votes, high school votes, and middle school
# votes.
class Students(db.Model):
    rollNo = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    splVotes = db.relationship('SplTable',backref='students')
    asplSrSecVotes = db.relationship('Aspl_Sr_Sec_Table',backref='students',cascade="all, delete-orphan")
    asplHSecVotes = db.relationship('Aspl_hSec_Table',backref='students',cascade="all, delete-orphan")
    asplMiddleVotes = db.relationship('Aspl_Middle_Table',backref='students',cascade="all, delete-orphan")

# The SplTable class represents a table in a database with columns for rollNo and splVotes, where
# rollNo is a foreign key referencing the rollNo column in the students table.
class SplTable(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    splVotes = db.Column(db.String(50),nullable=False)

# The class "Aspl_Sr_Sec_Table" represents a table in a database with columns for roll number and
# votes for a student in a senior secondary school.
class Aspl_Sr_Sec_Table(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    asplVotes = db.Column(db.String(50),nullable=False)

# The class "Aspl_hSec_Table" represents a table in a database with columns for roll number and votes
# for the ASPL (Assistant School Prefect) position.
class Aspl_hSec_Table(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    asplVotes = db.Column(db.String(50),nullable=False)

# The class "Aspl_Middle_Table" represents a middle table in a database with columns for rollNo and
# asplVotes.
class Aspl_Middle_Table(db.Model):
    rollNo = db.Column(db.Integer ,db.ForeignKey('students.rollNo'),primary_key=True)
    asplVotes = db.Column(db.String(50),nullable=False)

# The AdminTable class represents a table in a database with columns for an ID, username, and
# password.
class AdminTable(db.Model):
    _id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    passwd = db.Column(db.String(500),nullable=False)

# The class "CandidateDetails" represents a model for storing candidate details, including their name,
# position, and image name.
class CandidateDetails(db.Model):
    _id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    position = db.Column(db.String(100),nullable=False)
    imageName = db.Column(db.String(500),nullable=False)
    