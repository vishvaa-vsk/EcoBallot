import os
from os import environ, path
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(path.join(basedir,".env"))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://eElection:SKNSPMCvvJC-1975@localhost/eElection"
    #SQLALCHEMY_DATABASE_URI = "sqlite:///eElection.sqlite3"
    UPLOAD_FOLDER ='static/img'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True