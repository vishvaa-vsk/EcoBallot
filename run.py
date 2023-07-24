import os,time
basedir = os.path.abspath(os.path.dirname(__file__))

def installDependencies():
    requirementsFile=os.path.join(f"{basedir}/src/",'requirements.txt')
    if os.path.isfile(requirementsFile):
        os.system(f"pip install -r {requirementsFile}")

def setAppSecretKey():
    secretKey = os.urandom(24).hex()
    with open(os.path.join(f"{basedir}/src/",'.env'),"a+") as File:
        File.write(f"SECRET_KEY={secretKey}\n")
        File.write(f"FLASK_APP=src\n")

if __name__ == "__main__":
    try:
        installDependencies()
        if not os.path.isfile(os.path.join(f"{basedir}/src/",".env")):
            setAppSecretKey()
        time.sleep(1)
        os.system("flask --app src --debug run -h 0.0.0.0 -p 3030")
    except Exception as e:
        print(e)