# About EcoBallot
**EcoBallot**, a platform designed to revolutionize the way students participate in school elections.
This app was created in Python using the Flask Framework.

# Modules used
* Flask
* Flask-SQLAlchemy
* Flask-WTF
* mysql-connector and PyMySQL (For Mysql Database Connection)

# Requirements
- Python 3.10.6 or above 
- Any browser to access internet 
- Any Operating System with Python3 as mentioned

# How to use it?
> **_ADVICE_: Since this is a web application, I recommend you host this on dedicated server or in _WSGI Production Server_ for an easy access.**

> **_NOTE:_ Since EcoBallot.exe is unsigned, antivirus software may mistakenly identify it as malware. Allow it if you trust me or run the run.py to complete the work.**

The EcoBallot.exe file can be used to set up the necessary components and launch the standard Flask development server for testing.<br>

Or run the run.py file with 
```
python3 run.py
```
It will automatically open the browser with the app's url
****
# How to connect it to MySQL (not connected by default)

> This web application stores all the data in a database file called EcoBallot.sqlite by default.

To use MySQL Database, uncomment the config file's no 10<sup>th</sup> line

### Edit src/config.py file

**Uncomment this line (no 10<sup>th</sup> line)**
```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/database_name"
```

#### Replace the `username` to the username of MySQL, `password`,`localhost` and `database_name` with the created one.

#### **Make sure you comment the next line to avoid writing in the local file.
****

# Known issues
#### * Python not found or pip not found:
Usually, this error occurs when python is not installed in the PATH (if you did not check the add Python to the PATH during installation of python). You might get this error even you did the above mentioned.  

To solve this, Add the path of the python into your **_system PATH_** . Usually the path of python will be in `C:\users\your_name\AppData\Local\Programs\Python310\`
****
