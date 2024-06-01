# The code is importing all the models from the `models` module and the `generate_password_hash`
# function from the `werkzeug.security` module. This allows the code to access and use the classes and
# functions defined in those modules.
from .models import *
from werkzeug.security import generate_password_hash

def getClass(arg):
    """
    The function `getClass` retrieves the roll numbers and names of students whose roll numbers start
    with a given argument.
    
    :param arg: The parameter "arg" is a string that represents the prefix of the roll numbers you want
    to search for in the Students table
    :return: a list of tuples containing the roll number and name of students whose roll number starts
    with the given argument.
    """
    result = Students.query.with_entities(Students.rollNo , Students.name).filter(Students.rollNo.startswith(arg)).all()
    return result

def sendSPLData():
    """
    The function `sendSPLData` retrieves the names and image names of candidates with the position "SPL"
    from the `CandidateDetails` table.
    :return: The function `sendSPLData()` returns a list of tuples containing the name and imageName of
    candidates who have the position "SPL" in the `CandidateDetails` table.
    """
    spls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="SPL").all()
    return spls

def sendASPLMiddleData():
    """
    The function `sendASPLMiddleData` retrieves the names and image names of all candidates with the
    position "ASPL(Middle)" from the `CandidateDetails` table.
    :return: a list of tuples containing the name and imageName of all candidates who have the position
    "ASPL(Middle)" in the CandidateDetails table.
    """
    aspls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="ASPL(Middle)").all()
    return aspls

def sendASPLHsecData():
    """
    The function `sendASPLHsecData` retrieves the names and image names of all candidates with the
    position "ASPL(H.Sec)" from the `CandidateDetails` table.
    :return: a list of tuples containing the name and imageName of candidates who have the position
    "ASPL(H.Sec)".
    """
    aspls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="ASPL(H.Sec)").all()
    return aspls

def sendASPLSrSecData():
    """
    The function `sendASPLSrSecData` retrieves the names and image names of candidates who are applying
    for the position of ASPL (Sr.Sec).
    :return: a list of tuples containing the name and imageName of candidates who have the position
    "ASPL(Sr.Sec)".
    """
    aspls = CandidateDetails.query.with_entities(CandidateDetails.name,CandidateDetails.imageName).filter(CandidateDetails.position=="ASPL(Sr.Sec)").all()
    return aspls

def setAdmin():
    """
    The function `setAdmin()` sets the username and password for an admin user and adds it to the admin
    table in the database.
    """
    username,passwd = "admin","scrypt:32768:8:1$p7miDfAcC5ufDc7c$c96867238b5b078157655cde6e426cfb52601ca67b5b396e6641428de381527f5b051fc4435b1108af40ea0a9f6e2b683642ad7caefb2cc0f32f9f59492759c9"
    admin = AdminTable(username=username,passwd=passwd)
    db.session.add(admin)

def getWinnerPhoto(winner):
    """
    The function `getWinnerPhoto` retrieves the image name of a candidate who is the winner.
    
    :param winner: The "winner" parameter is the name of the candidate who won the election
    :return: the imageName of the candidate who is the winner.
    """
    getPhoto = CandidateDetails.query.with_entities(CandidateDetails.imageName).filter(CandidateDetails.name==winner).first()
    return getPhoto[0]

def getSplResults():
    """
    The function `getSplResults` retrieves the names of candidates running for the position "SPL" from
    the `CandidateDetails` table, counts the number of votes each candidate received from the `SplTable`
    table, and returns a dictionary with the candidate names as keys and their respective vote counts as
    values.
    :return: The function `getSplResults` returns a dictionary `finalResult` which contains the number
    of votes each candidate received in the SPL election. The keys of the dictionary are the names of
    the candidates, and the values are the corresponding vote counts.
    """
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="SPL").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candi in Candidates:
        candidateVotes = SplTable.query.filter_by(splName=candi).count()
        finalResult[candi] = candidateVotes
    return finalResult

def getAspl_Sr_Sec_Results():
    """
    The function `getAspl_Sr_Sec_Results` retrieves the names of candidates running for the position of
    ASPL (Sr.Sec) and counts the number of votes each candidate received.
    :return: a dictionary containing the final results of the ASPL (Sr. Sec) election. The keys of the
    dictionary are the names of the candidates, and the values are the number of votes each candidate
    received.
    """
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="ASPL(Sr.Sec)").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candidate in Candidates:
        candidateVotes = Aspl_Sr_Sec_Table.query.filter_by(asplName=candidate).count()
        finalResult[candidate] = candidateVotes
    return finalResult

def getAspl_hSec_Results():
    """
    The function `getAspl_hSec_Results` retrieves the vote count for each candidate running for the
    position of ASPL(H.Sec) and returns the results as a dictionary.
    :return: a dictionary containing the final results of the ASPL(H.Sec) election. The keys of the
    dictionary are the names of the candidates, and the values are the number of votes each candidate
    received.
    """
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="ASPL(H.Sec)").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candidate in Candidates:
        candidateVotes = Aspl_hSec_Table.query.filter_by(asplName=candidate).count()
        finalResult[candidate] = candidateVotes
    return finalResult

def getAspl_Middle_Results():
    """
    The function `getAspl_Middle_Results` retrieves the names of candidates running for the position of
    ASPL(Middle) and counts the number of votes each candidate has received.
    :return: a dictionary containing the final results of the ASPL(Middle) position. The keys of the
    dictionary are the names of the candidates, and the values are the number of votes each candidate
    received.
    """
    Candidates = []
    getCandidates = CandidateDetails.query.with_entities(CandidateDetails.name).filter(CandidateDetails.position=="ASPL(Middle)").all()
    for candidates in getCandidates:
        for candidate in candidates:
            Candidates.append(candidate)
    finalResult = dict()
    for candidate in Candidates:
        candidateVotes = Aspl_Middle_Table.query.filter_by(asplName=candidate).count()
        finalResult[candidate] = candidateVotes
    return finalResult

def getLevel(roll):
    """
    The function `getLevel` takes a roll number as input and returns the level of the student based on
    the roll number.
    
    :param roll: The `roll` parameter is a string representing a student's roll number
    :return: a string indicating the level based on the given roll number. The possible return values
    are "Middle", "Higher", "Senior", or "Fake".
    """
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
