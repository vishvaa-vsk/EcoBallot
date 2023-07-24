from flask import Blueprint,flash,render_template,url_for,session,redirect,request
from ..extensions import db
from ..models import *
from ..helper import *
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,SelectField
from wtforms.validators import DataRequired,InputRequired
from werkzeug.utils import secure_filename
import os
from ..config import Config
from werkzeug.security import generate_password_hash,check_password_hash

admin = Blueprint("admin",__name__,url_prefix="/admin")

class AddStudentsForm(FlaskForm):
    Candidatename = StringField("Enter the Candidate Name",validators=[DataRequired()])
    position = SelectField("Select Position",validators=[InputRequired()],choices=["SPL","ASPL(Middle)","ASPL(H.Sec)","ASPL(Sr.Sec)"])
    file = FileField("Image",validators=[InputRequired()])
    submit = SubmitField("Submit")

@admin.route("/",methods=["GET","POST"])
def adminLogin():
    if not db.session.query(db.session.query(AdminTable).filter(AdminTable.username == "admin").exists()).scalar():
        setAdmin()
    if request.method == "POST":
        session.permanent = True
        username,passwd = request.form["username"],request.form["passwd"]
        user = db.session.query(AdminTable).filter(AdminTable.username == username).first()
        if check_password_hash(user.passwd,passwd):
            session["adminLogin"] = True
            session["adminName"] = username
            return redirect(url_for("admin.adminDashBoard"))
        else:
            flash("Username or password not exists!")
    return render_template("admin/adminLogin.html")

@admin.route("/dashboard",methods=["GET","POST"])
def adminDashBoard():
    if "adminLogin" in session:
        username = session["adminName"]
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/adminDashboard.html",name=username)

@admin.route("/newAdmin",methods=["GET","POST"])
def newAdmin():
    if request.method == "POST":
        if "adminLogin" in session:
            username,passwd = request.form["username"],request.form["passwd"]
            hashed_value = generate_password_hash(passwd , method='scrypt')
            try:
                addNewAdmin = AdminTable(username=username,passwd=hashed_value)
                db.session.add(addNewAdmin)
            except Exception as e:
                flash(e)
            else:
                flash("Internal Server error")
        else:
            return redirect(url_for("admin.adminLogin"))
    return render_template("admin/newAdmin.html")

@admin.route("/viewAdmins",methods=["GET","POST"])
def viewAdmins():
    if "adminLogin" in session:
        getAdminDetails = AdminTable.query.with_entities(AdminTable.username).all()
        return render_template("admin/viewAdmin.html",adminList = getAdminDetails)
    else: 
        return redirect(url_for("admin.adminLogin"))

@admin.route("/splResults",methods=["GET","POST"])
def splResult():
    if "adminLogin" in session:
       totalVotes = SplTable.query.count()
       result = getSplResults()
       winners = [key for key, value in result.items() if value == max(result.values())]
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/splResults.html",total_votes=totalVotes,result=result,winners=winners)

@admin.route("/asplMiddleResults",methods=["GET","POST"])
def asplMiddleResult():
    if "adminLogin" in session:
       totalVotes = Aspl_Middle_Table.query.count()
       result = getAspl_Middle_Results()
       winners = [key for key, value in result.items() if value == max(result.values())]
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/asplResults.html",total_votes=totalVotes,result=result,winners=winners)

@admin.route("/asplHsecResults",methods=["GET","POST"])
def asplHsecResult():
    if "adminLogin" in session:
       totalVotes = Aspl_hSec_Table.query.count()
       result = getAspl_hSec_Results()
       winners = [key for key, value in result.items() if value == max(result.values())]
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/asplResults.html",total_votes=totalVotes,result=result,winners=winners)

@admin.route("/asplSrSecResults",methods=["GET","POST"])
def asplSrSecResult():
    if "adminLogin" in session:
       totalVotes = Aspl_Sr_Sec_Table.query.count()
       result = getAspl_Sr_Sec_Results()
       winners = [key for key, value in result.items() if value == max(result.values())]
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/asplResults.html",total_votes=totalVotes,result=result,winners=winners)

@admin.route('/votedStudents',methods=['GET', 'POST'])
def viewStudents():
    if "adminLogin" in session:
        eight = getClass("8")
        nine = getClass("9")
        ten = getClass("10")
        eleven = getClass("11")
        tweleve = getClass("12")
    return render_template("admin/viewStudents.html",eight=eight,nineth=nine,tenth=ten,eleventh=eleven,tweleveth=tweleve)
    
    
@admin.route("/addCandidateDetails",methods=['GET', 'POST'])
def addCandidateDetails():
    if "adminLogin" in session:
        form = AddStudentsForm()
        if request.method == "POST":
            if form.validate_on_submit():
                name = str(form.Candidatename.data).title()
                position = str(form.position.data)
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(os.path.join('src/static/img/',filename))
                addCandidate = CandidateDetails(name=name,position=position,imageName=str(filename))
                db.session.add(addCandidate)
                form.Candidatename.data =''
                form.position.data =''
                flash("Added succesfully")
        return render_template("admin/addCandidates.html",form = form)
    else:
        return redirect(url_for("admin.adminLogin"))