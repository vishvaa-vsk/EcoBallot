import os,time
import mysql.connector as mysql
import platform
from os import environ, path
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(path.join(basedir,".env"))

def installDependencies():
    requirementsFile =os.path.join(basedir,'requirements.txt')
    if os.path.isfile(requirementsFile):
        os.system(f"pip install -r {requirementsFile}")
          
def setFlaskApp():
    if os.path.isfile(os.path.join(basedir,'.env')):
        secretKey = os.urandom(24).hex()
        with open(os.path.join(basedir,'.env'),"a+") as File:
            File.write(f"SECRET_KEY={secretKey}\n")
            File.write(f"FLASK_APP=src\n")
        
def setEnvironVariables():
    if platform.system() == "Linux":
        os.system(f"export FLASK_APP={environ.get('FLASK_APP')}")
        os.system(f"export FLASK_DEBUG=1")
        os.system("flask --app src run -h 0.0.0.0 -p 3030")
    elif platform.system() == "Windows":
        os.system(f"set FLASK_APP={environ.get('FLASK_APP')}")
        os.system(f"set FLASK_DEBUG=1")
        os.system("flask --app src run -h 0.0.0.0 -p 3030")
    

if __name__ == "__main__":
    try:
        installDependencies()
        setFlaskApp()
        time.sleep(1.5)
        setEnvironVariables()
    except Exception as e:
        print(e)

