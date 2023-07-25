# The code `import os,time` imports the `os` and `time` modules in Python.
import os,time
basedir = os.path.abspath(os.path.dirname(__file__))

def installDependencies():
    """
    The function installs the dependencies listed in the requirements.txt file.
    """
    requirementsFile=os.path.join(f"{basedir}/src/",'requirements.txt')
    if os.path.isfile(requirementsFile):
        os.system(f"pip install -r {requirementsFile}")

def setAppSecretKey():
    """
    The function `setAppSecretKey` generates a random secret key and writes it to a .env file along with
    the FLASK_APP variable.
    """
    secretKey = os.urandom(24).hex()
    with open(os.path.join(f"{basedir}/src/",'.env'),"a+") as File:
        File.write(f"SECRET_KEY={secretKey}\n")
        File.write(f"FLASK_APP=src\n")

# The code `if __name__ == "__main__":` is a common Python idiom that checks if the current script is
# being run as the main module. In other words, it checks if the script is being executed directly and
# not imported as a module.
if __name__ == "__main__":
    try:
        installDependencies()
        if not os.path.isfile(os.path.join(f"{basedir}/src/",".env")):
            setAppSecretKey()
        time.sleep(1)
        os.system("flask --app src --debug run -h 0.0.0.0 -p 3030")
    except Exception as e:
        print(e)