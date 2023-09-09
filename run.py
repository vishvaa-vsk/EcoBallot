# The code `import os,time` imports the `os` and `time` modules in Python.
import os,time,socket,webbrowser

ip = socket.gethostbyname(socket.gethostname())
basedir = os.path.abspath(os.path.dirname(__file__))

def installDependencies():
    """
    The function installs the dependencies listed in the requirements.txt file.
    """
    """
    The function installs the dependencies listed in the requirements.txt file.
    """
    requirementsFile=os.path.join(f"{basedir}/src/",'requirements.txt')
    if os.path.isfile(requirementsFile):
        os.system(f"pip install -r {requirementsFile}")

def setAppSecretKey():
    """
    The `setAppSecretKey` function generates a random secret key and writes it to a .env file along with
    the FLASK_APP variable.
    """
    """
    The function `setAppSecretKey` generates a random secret key and writes it to a .env file along with
    the FLASK_APP variable.
    """
    secretKey = os.urandom(24).hex()
    with open(os.path.join(f"{basedir}/src/",'.env'),"a+") as File:
        File.write(f"SECRET_KEY={secretKey}\n")
        File.write(f"FLASK_APP=src\n")


# The code block `if __name__ == "__main__":` is a common idiom in Python that allows a module to be
# run as a standalone script or imported as a module.
if __name__ == "__main__":
    try:
        installDependencies()
        if not os.path.isfile(os.path.join(f"{basedir}/src/",".env")):
            setAppSecretKey()
        if not os.path.isdir(f"{basedir}/src/static/img"):
            os.mkdir(f"{basedir}/src/static/img")
        time.sleep(1)
        webbrowser.open(f"http://{ip}:3030/")
        os.system("flask --app src --debug run -h 0.0.0.0 -p 3030")
        
    except KeyboardInterrupt:
        os.system(f"del {basedir}/src/.env")
    else:
        print("Program Failed!")