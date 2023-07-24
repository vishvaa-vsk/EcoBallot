from .models import *
from werkzeug.security import generate_password_hash

def getClass(arg):
    result = Students.query.with_entities(Students.rollNo , Students.name).filter(Students.rollNo.startswith(arg)).all()
    return result

def sendSPLData():
    spls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="SPL").all()
    return spls

def sendASPLMiddleData():
    aspls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="ASPL(Middle)").all()
    return aspls

def sendASPLHsecData():
    aspls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="ASPL(H.Sec)").all()
    return aspls

def sendASPLSrSecData():
    aspls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="ASPL(Sr.Sec)").all()
    return aspls

def setAdmin():
    username,passwd = "admin",generate_password_hash("sknspmc@1975",method="scrypt")
    admin = AdminTable(username=username,passwd=passwd)
    db.session.add(admin)

def getSplResults():
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="SPL").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candi in Candidates:
        candidateVotes = SplTable.query.filter_by(splVotes=candi).count()
        finalResult[candi] = candidateVotes
    return finalResult

def getAspl_Sr_Sec_Results():
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="ASPL(Sr.Sec)").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candidate in Candidates:
        candidateVotes = Aspl_Sr_Sec_Table.query.filter_by(asplVotes=candidate).count()
        finalResult[candidate] = candidateVotes
    return finalResult

def getAspl_hSec_Results():
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="ASPL(H.Sec)").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candidate in Candidates:
        candidateVotes = Aspl_hSec_Table.query.filter_by(asplVotes=candidate).count()
        finalResult[candidate] = candidateVotes
    return finalResult

def getAspl_Middle_Results():
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="ASPL(Middle)").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candidate in Candidates:
        candidateVotes = Aspl_Middle_Table.query.filter_by(asplVotes=candidate).count()
        finalResult[candidate] = candidateVotes
    return finalResult

def getLevel(roll):
    if len(roll) == 4:
        if roll[1] != "0":
            if roll[0] == "8":
                return "Middle"
            elif roll[0] == "9":
                return "Higher"
        else:
            return "Fake"
    else:
        if roll[:2] == "10":
            return "Higher"
        if roll[:2] == "11" or roll[:2] == "12":
            return "Senior"
        else:
            return "Fake"
        
