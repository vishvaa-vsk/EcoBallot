from flask import Blueprint,flash,render_template,url_for,session,redirect,request,jsonify
from ..extensions import db
from ..models import *
from ..helper import *
from datetime import date
todays_date = date.today()

main = Blueprint("main",__name__)

@main.route("/home",methods=["GET","POST"])
@main.route("/",methods=["GET","POST"])
def login():
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
        else:
            new_user = Students(rollNo=int(rollNo),name=str(name))
            db.session.add(new_user)
            session["rollNo"] = rollNo
            session["name"] = name
            return redirect(url_for("main.asplMiddleVote"))
    return render_template("index.html",year=todays_date.year)

@main.route("/splVote",methods=["GET","POST"])
def splVote():
    splData = sendSPLData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if db.session.query(db.session.query(Students).filter_by(rollNo=int(rollNo)).exists()).scalar():
            if request.method == "POST":
                if request.form.get('userVote') != None:
                    userVote = request.form.get('userVote')
                    try:
                        addVote = SplTable(rollNo=int(rollNo) , splVotes=userVote)
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
    aspldata = sendASPLMiddleData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if getLevel(rollNo) == "Middle":
            if db.session.query(db.session.query(Students).filter_by(rollNo=rollNo).exists()).scalar():
                if request.method == "POST":
                    if request.form.get('userVote') != None:
                        userVote = request.form.get('userVote')
                        try:
                            addVote = Aspl_Middle_Table(rollNo=rollNo , asplVotes=userVote)
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
    aspldata = sendASPLHsecData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if getLevel(rollNo) == "Higher":
            if db.session.query(db.session.query(Students).filter_by(rollNo=rollNo).exists()).scalar():
                if request.method == "POST":
                    if request.form.get('userVote') != None:
                        userVote = request.form.get('userVote')
                        try:
                            addVote = Aspl_hSec_Table(rollNo=rollNo,asplVotes=userVote)
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
    aspldata = sendASPLSrSecData()
    if "rollNo" and "name" in session:
        rollNo = session["rollNo"]
        if getLevel(rollNo) == "Senior":
            if db.session.query(db.session.query(Students).filter_by(rollNo=rollNo).exists()).scalar():
                if request.method == "POST":
                    if request.form.get('userVote') != None:
                        userVote = request.form.get('userVote')
                        try:
                            addVote = Aspl_Sr_Sec_Table(rollNo=rollNo,asplVotes=userVote)
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
    [session.pop(key) for key in list(session.keys())]
    return redirect(url_for("main.login"))

@main.route("/success", methods=["GET","POST"])
def voteSuccess():
    if "name" and "rollNo" in session:
        name = session["name"]
        return render_template("success.html",name=name)
    else:
        return redirect(url_for("main.login"))