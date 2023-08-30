# This line of code is importing various modules and classes from different files and libraries.
from flask import Blueprint,flash,render_template,url_for,session,redirect,request,jsonify
from ..extensions import db
from ..models import *
from ..helper import *
from datetime import date
# The line `todays_date = date.today()` is assigning the current date to the variable `todays_date`.
# The `date.today()` function is a method from the `datetime` module that returns the current local
# date as a `date` object.
todays_date = date.today()
# 
# The line `main = Blueprint("main",__name__)` is creating a Blueprint object named "main".
main = Blueprint("main",__name__)

@main.route("/home",methods=["GET","POST"])
@main.route("/",methods=["GET","POST"])
def login():
    """
    The `login` function checks if a user has already voted, and if not, adds the user to the database
    and redirects them to the appropriate voting page based on their level.
    :return: The code is returning a redirect to different routes based on certain conditions. If the
    request method is "POST" and the student has already voted, it flashes a message "Already Voted!".
    If the student's level is "Higher" or "Senior", it adds the student to the database, sets session
    variables for rollNo and name, and redirects to the "main.splVote" route.
    """
    if request.method == "POST":
        session.permanent = True
        name,rollNo = request.form["studName"].title(),request.form["rollNo"]
        exists = db.session.query(db.session.query(Students).filter_by(rollNo=rollNo).exists()).scalar()
        if exists:
            flash("Aldready Voted!")
        elif getLevel(rollNo) == "Higher" or getLevel(rollNo) == "Senior":
            new_user = Students(rollNo=int(rollNo),name=str(name))
            db.session.add(new_user)
            session["rollNo"] = rollNo
            session["name"] = name
            return redirect(url_for("main.splVote"))
        elif getLevel(rollNo) == "Middle":
            new_user = Students(rollNo=int(rollNo),name=str(name))
            db.session.add(new_user)
            session["rollNo"] = rollNo
            session["name"] = name
            return redirect(url_for("main.asplMiddleVote"))
        else:
            return "<h1>You are trying to cheat 😡</h1>"
    return render_template("index.html",year=todays_date.year)

@main.route("/splVote",methods=["GET","POST"])
def splVote():
    """
    The function `splVote()` checks if a user is logged in, retrieves special data, and allows the user
    to vote, redirecting them to different URLs based on their level.
    :return: either a redirect to the login page or a rendered template "splVote.html" with the data
    variable passed to it.
    """
    splData = sendSPLData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if db.session.query(db.session.query(Students).filter_by(rollNo=int(rollNo)).exists()).scalar():
            if request.method == "POST":
                if request.form.get('userVote') != None:
                    userVote = request.form.get('userVote')
                    try:
                        addVote = SplTable(rollNo=int(rollNo) , splName=userVote)
                        db.session.add(addVote)
                    except Exception as e:
                        flash(str(e))
                if getLevel(rollNo) == "Senior":
                    return jsonify({'url':"/asplSrSecVote"})
                else:
                    return jsonify({'url':"/asplHsecVote"})
    else:
        return redirect(url_for('main.login'))
    return render_template("splVote.html",data = splData)

@main.route("/asplMiddleVote",methods=["GET","POST"])
def asplMiddleVote():
    """
    The function `asplMiddleVote` allows a middle-level student to vote in the ASPL (Assistant School
    Prefects) election and stores their vote in the database.
    :return: either a JSON response with a URL to "/success" or a string "<h1>You are trying to cheat
    😡</h1>".
    """
    aspldata = sendASPLMiddleData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if getLevel(rollNo) == "Middle":
            if db.session.query(db.session.query(Students).filter_by(rollNo=rollNo).exists()).scalar():
                if request.method == "POST":
                    if request.form.get('userVote') != None:
                        userVote = request.form.get('userVote')
                        try:
                            addVote = Aspl_Middle_Table(rollNo=rollNo , asplName=userVote)
                            db.session.add(addVote)
                        except:
                            flash("Internal server error")
                    return jsonify({'url':"/success"})
        else:
            return "<h1>You are trying to cheat 😡</h1>"
    else:
        return redirect(url_for("main.login"))
    return render_template("asplMiddleVote.html",data=aspldata)

@main.route("/asplHsecVote",methods=["GET","POST"])
def asplHsecVote():
    """
    The function `asplHsecVote` checks if the user is logged in and has the appropriate level of access,
    and then allows them to vote in the ASPL Higher Secondary election.
    :return: either a JSON response with a URL to "/success" or a rendered HTML template
    "asplHsecVote.html" with the data variable.
    """
    aspldata = sendASPLHsecData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if getLevel(rollNo) == "Higher":
            if db.session.query(db.session.query(Students).filter_by(rollNo=rollNo).exists()).scalar():
                if request.method == "POST":
                    if request.form.get('userVote') != None:
                        userVote = request.form.get('userVote')
                        try:
                            addVote = Aspl_hSec_Table(rollNo=rollNo,asplName=userVote)
                            db.session.add(addVote)
                        except:
                            flash("Internal server error")
                    return jsonify({'url':"/success"})
        else:
            return "<h1>You are trying to cheat 😡</h1>"
    else:
        return redirect(url_for("main.login"))
    return render_template("asplHsecVote.html",data=aspldata)

@main.route("/asplSrSecVote",methods=["GET","POST"])
def asplSrSecVote():
    """
    The function `asplSrSecVote` handles the voting process for senior secondary students and checks for
    authentication and authorization before allowing the vote.
    :return: either a JSON response with a URL to "/success" or a string "<h1>You are trying to cheat
    😡</h1>".
    """
    aspldata = sendASPLSrSecData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if getLevel(rollNo) == "Senior":
            if db.session.query(db.session.query(Students).filter_by(rollNo=rollNo).exists()).scalar():
                if request.method == "POST":
                    if request.form.get('userVote') != None:
                        userVote = request.form.get('userVote')
                        try:
                            addVote = Aspl_Sr_Sec_Table(rollNo=rollNo,asplName=userVote)
                            db.session.add(addVote)
                        except:
                            flash("Internal server error")
                    return jsonify({'url':"/success"})
        else:
            return "<h1>You are trying to cheat 😡</h1>"
    else:
        return redirect(url_for("main.login"))
    return render_template("asplSrSecVote.html",data=aspldata)


@main.route("/logout")
def logout():
    """
    The `logout` function clears the session and redirects the user to the login page.
    :return: a redirect to the login page.
    """
    [session.pop(key) for key in list(session.keys())]
    return redirect(url_for("main.login"))

@main.route("/success", methods=["GET","POST"])
def voteSuccess():
    """
    The function checks if the "name" and "rollNo" keys are present in the session dictionary, and if
    so, it returns a rendered template with the name variable passed to it, otherwise it redirects to
    the login page.
    :return: either the rendered template "success.html" with the variable "name" passed to it, or it is
    redirecting to the "login" route.
    """
    if "name" and "rollNo" in session:
        name = session["name"]
        return render_template("success.html",name=name)
    else:
        return redirect(url_for("main.login"))