import requests
from getopt import getopt, GetoptError
from sys import argv, exit
import pyexcel as pe


def getHelp():
    print(
        'python paycheck_upload.py' +
        ' -l <loginUrl> -d <documentsUrl> -u <username> -p <password> -f <filesDir>'
        )


def main(argument):

    path_to_files = ""

    try:
        opts, args = getopt(argument, "hl:d:u:p:f:", [
            "loginUrl=",
            "documentsUrl=",
            "username=",
            "password=",
            "filesDir="])
    except GetoptError:
        getHelp()
        exit(2)

    for opt, arg in opts:
        if opt == '-h':
            getHelp()
            exit()
        elif opt in ("-l", "--loginUrl"):
            loginUrl = arg
        elif opt in ("-d", "--documentsUrl"):
            documentsUrl = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-f", "--filesDir"):
            path_to_files = arg

    r = requests.post(
        loginUrl,
        data={
            'email': username,
            'password': password},
        headers={
            "Content-Type": "application/x-www-form-urlencoded"}
        )

    # ToDo: Iterar desde acá hasta el final por cada archivo pdf que exista
    #   en path_to_files
    f = open(path_to_files + '20-29087702-5_20210208_0_711521050.pdf', 'rb'),

    files = {
        'file': (
            f[0].name,
            f[0],
            'file/pdf',
        )}

    headers = {
        "Accept": "text/html, application/json",
        "Cookie": r.headers["Set-Cookie"],
        }

    # ToDo: Crear un listado excel con los cuil de los empleados y sus employeeId
    #   buscar en la lista el employeeId en base al cuil del nombre del archivo
    #   pdf y ponerlo en el diccionario "data"
    data = {
        "employeeId": "395",
        "name": "Recibo",
        "MAX_FILE_SIZE": "2000000",
        }

    x = requests.post(
        documentsUrl,
        data=data,
        headers=headers,
        files=files,
        )


if __name__ == "__main__":
    main(argv[1:])
