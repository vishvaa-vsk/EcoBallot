# This code is importing various modules and classes from different libraries that are used in the
# Flask application.
from flask import Blueprint,flash,render_template,url_for,session,redirect,request
from ..extensions import db
from ..models import *
from ..helper import *
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,FileField,SelectField
from wtforms.validators import DataRequired,InputRequired
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash,check_password_hash

# The line `admin = Blueprint("admin",__name__,url_prefix="/admin")` is creating a Blueprint object
# named "admin".
admin = Blueprint("admin",__name__,url_prefix="/admin")

# The `AddStudentsForm` class is a Flask form that allows users to enter a candidate's name, select a
# position, and upload an image.
class AddStudentsForm(FlaskForm):
    Candidatename = StringField("Enter the Candidate Name",validators=[DataRequired()])
    position = SelectField("Select Position",validators=[InputRequired()],choices=["SPL","ASPL(Middle)","ASPL(H.Sec)","ASPL(Sr.Sec)"])
    file = FileField("Image",validators=[InputRequired()])
    submit = SubmitField("Submit")

@admin.route("/",methods=["GET","POST"])
def adminLogin():
    """
    The function `adminLogin` is responsible for handling the login functionality for the admin user.
    :return: the rendered template "admin/adminLogin.html" if the request method is not "POST". If the
    request method is "POST" and the username and password provided match the admin credentials stored
    in the database, the function redirects to the "admin.adminDashBoard" route. If the username and
    password do not match, a flash message is displayed and the same template is rendered again.
    """
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
    """
    The function adminDashBoard checks if the user is logged in as an admin and redirects to the admin
    login page if not, otherwise it renders the admin dashboard template with the admin's username.
    :return: the rendered template "admin/adminDashboard.html" with the variable "name" set to the value
    of the "username" variable.
    """
    if "adminLogin" in session:
        username = session["adminName"]
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/adminDashboard.html",name=username)

@admin.route("/newAdmin",methods=["GET","POST"])
def newAdmin():
    """
    The function `newAdmin` is used to add a new admin to the AdminTable in a Flask application, after
    hashing the password.
    :return: the rendered template "admin/newAdmin.html".
    """
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
    """
    The function "viewAdmins" checks if the user is logged in as an admin, and if so, retrieves the
    usernames of all admins from the AdminTable and renders them in the "admin/viewAdmin.html" template.
    If the user is not logged in as an admin, it redirects them to the adminLogin page.
    :return: either the rendered template "admin/viewAdmin.html" with the adminList variable set to the
    result of the query, or it is redirecting to the "admin.adminLogin" route.
    """
    if "adminLogin" in session:
        getAdminDetails = AdminTable.query.with_entities(AdminTable.username).all()
        return render_template("admin/viewAdmin.html",adminList = getAdminDetails)
    else: 
        return redirect(url_for("admin.adminLogin"))

@admin.route("/splResults",methods=["GET","POST"])
def splResult():
    """
    The function `splResult` checks if the user is logged in as an admin, retrieves the total votes and
    results of a special election, determines the winner(s), and returns the rendered template with the
    winner's image, total votes, results, and winners.
    :return: a rendered template with the variables `winnerImage`, `total_votes`, `result`, and
    `winners`.
    """
    if "adminLogin" in session:
       totalVotes = SplTable.query.count()
       result = getSplResults()
       winners = [key for key, value in result.items() if value == max(result.values())]
       winnerImage = getWinnerPhoto(winners[0])
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/splResults.html",winnerImage=winnerImage,total_votes=totalVotes,result=result,winners=winners)

@admin.route("/asplMiddleResults",methods=["GET","POST"])
def asplMiddleResult():
    """
    This function retrieves the total votes and results for the ASPL middle category, determines the
    winner(s), and renders the admin ASPL results page with the winner's photo, total votes, results,
    and winners.
    :return: a rendered template with the variables winnerImage, total_votes, result, and winners.
    """
    if "adminLogin" in session:
       totalVotes = Aspl_Middle_Table.query.count()
       result = getAspl_Middle_Results()
       winners = [key for key, value in result.items() if value == max(result.values())]
       winnerImage = getWinnerPhoto(winners[0])
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/asplResults.html",winnerImage=winnerImage,total_votes=totalVotes,result=result,winners=winners)

@admin.route("/asplHsecResults",methods=["GET","POST"])
def asplHsecResult():
    """
    The function `asplHsecResult` checks if the user is logged in as an admin, retrieves the total votes
    and results for a specific table, determines the winner(s) based on the highest vote count,
    retrieves the photo of the winner, and renders a template with the total votes, winner image,
    results, and winners.
    :return: a rendered template "admin/asplResults.html" with the following variables: total_votes,
    winnerImage, result, and winners.
    """
    if "adminLogin" in session:
       totalVotes = Aspl_hSec_Table.query.count()
       result = getAspl_hSec_Results()
       winners = [key for key, value in result.items() if value == max(result.values())]
       winnerImage = getWinnerPhoto(winners[0])
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/asplResults.html",total_votes=totalVotes,winnerImage=winnerImage,result=result,winners=winners)

@admin.route("/asplSrSecResults",methods=["GET","POST"])
def asplSrSecResult():
    """
    The function `asplSrSecResult` checks if the user is logged in as an admin, retrieves the total
    votes and results for the ASPL Senior Secondary election, determines the winner(s), and renders the
    admin results page with the necessary data.
    :return: a rendered template with the variables `total_votes`, `winnerImage`, `result`, and
    `winners`.
    """
    if "adminLogin" in session:
       totalVotes = Aspl_Sr_Sec_Table.query.count()
       result = getAspl_Sr_Sec_Results()
       winners = [key for key, value in result.items() if value == max(result.values())]
       winnerImage = getWinnerPhoto(winners[0])
    else:
        return redirect(url_for("admin.adminLogin"))
    return render_template("admin/asplResults.html",total_votes=totalVotes,winnerImage=winnerImage,result=result,winners=winners)

@admin.route('/votedStudents',methods=['GET', 'POST'])
def viewStudents():
    """
    The function "viewStudents" retrieves class information for different grades and renders a template
    to display the students.
    :return: the rendered template "admin/viewStudents.html" with the variables eight, nine, ten,
    eleven, and tweleve.
    """
    if "adminLogin" in session:
        eight = getClass("8")
        nine = getClass("9")
        ten = getClass("10")
        eleven = getClass("11")
        tweleve = getClass("12")
    return render_template("admin/viewStudents.html",eight=eight,nineth=nine,tenth=ten,eleventh=eleven,tweleveth=tweleve)
    
    
@admin.route("/addCandidateDetails",methods=['GET', 'POST'])
def addCandidateDetails():
    """
    The function `addCandidateDetails` adds candidate details to a database if the user is logged in as
    an admin.
    :return: a rendered template "admin/addCandidates.html" with the form as a parameter.
    """
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