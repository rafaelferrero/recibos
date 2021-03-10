import requests
from getopt import getopt, GetoptError
from sys import argv, exit
import pyexcel as pe
from os import listdir, path
from datetime import datetime as dt
import json


LOG_ERROR_PATH = "C:\\Users\\rostagnof\\Downloads\\UploadRecibos\\"


def get_str_timestamp():
    return str(dt.now())


def logerror(mensaje):
    with open(LOG_ERROR_PATH + "error_exportacion.txt", "a") as f:
        f.write("<<<" + get_str_timestamp() + ">>>   "+ mensaje + "\n")


def getHelp():
    print(
        'INSTRUCTIONS\n' +
        '============\n \n' +
        'First you need to install requirements: \n' +
        '   pip install -r requirements.txt \n \n' +
        'All the files in filesDir must be PDF.\n \n' +
        'Command Example: \n' +
        '   python paycheck_upload.py' +
        ' -a <apiUrl> -d <documentsUrl> -u <username> -p <password> -f <filesDir>\n'
        '   ================================================== \n' +
        '   =          All Parameters are requiered          = \n' +
        '   ================================================== \n \n'
        )


def getJson(rp,documentsUrl):
    p = 1
    x = requests.get(
        documentsUrl + "/employees/?page=" + str(p),
        headers = {
            "Accept": "text/html, application/json",
            "Cookie": rp.headers["Set-Cookie"],
            }
        )
    jsondata = json.loads(x.text)

    result = {}
    while jsondata["init"]["data"]:
        for i in range(len(jsondata["init"]["data"])):
            result[jsondata["init"]["data"][i]["init"]["taxId"]] = jsondata["init"]["data"][i]["init"]["id"]
        p += 1
        x = requests.get(
            documentsUrl + "/employees/?page=" + str(p),
            headers = {
                "Accept": "text/html, application/json",
                "Cookie": rp.headers["Set-Cookie"],
                }
            )
        jsondata = json.loads(x.text)

    return result


def get_employId(file, data):
    cuil = file[0:13].replace("-","")
    try:
        eid=data[cuil]
    except:
        eid=None

    return eid


def main(argument):

    apiUrl = ""
    documentsUrl = ""
    username = ""
    password = ""
    path_to_files = ""

    try:
        opts, args = getopt(argument, "ha:d:u:p:f:", [
            "apiUrl=",
            "documentsUrl=",
            "username=",
            "password=",
            "filesDir="])
    except GetoptError:
        getHelp()
        exit(2)

    if not opts:
        logerror("<<<No execution !!! The Parameters are not optionals !!!>>>")
        getHelp()
        exit(2)

    for opt, arg in opts:
        if opt == '-h':
            getHelp()
            exit()
        elif opt in ("-a", "--apiUrl"):
            apiUrl = arg
        elif opt in ("-d", "--documentsUrl"):
            documentsUrl = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-f", "--filesDir"):
            path_to_files = arg

    # All this fields are requiered
    if (apiUrl or documentsUrl or username or password or filesDir) == "":
        print("apiUrl={}\n" +
            "documentsUrl={}\n"+
            "username={}\n"+
            "password={}\n"+
            "filesDir".format(
                apiUrl, documentsUrl, username, password
            ))
        getHelp()
        exit(2)


    # All the files must be pdf
    flag = False
    files = listdir(path_to_files)
    for f in files:
        if path.splitext(f)[1] != ".pdf":
            flag = True
            logerror(f + " is not a 'PDF' file.")
    if flag:
        logerror("<<<No execution !!! all files must be 'PDF'>>>")
        getHelp()
        exit(2)

    r = requests.post(
        apiUrl + "/login",
        data={
            'email': username,
            'password': password},
        headers={
            "Content-Type": "application/x-www-form-urlencoded"}
        )

    employees = getJson(r, documentsUrl)
    logerror("Empleados a procesar {}\n \n".format(
        json.dumps(employees, indent=4)))

    logerror("Inicio proceso de upload de archivos")
    for file in files:
        # f = open(path_to_files + '20-29087702-5_20210208_0_711521050.pdf', 'rb'),
        f = open(path_to_files + file, 'rb'),
        print("    Uploading archivo {}".format(f[0].name))
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

        eid = get_employId(file, employees)
        data = {
            "employeeId": eid,
            "name": "Recibo",  # fixed
            "MAX_FILE_SIZE": "2000000",  # fixed
            }
        if eid:
            u = requests.post(
                documentsUrl + "/documents",
                data=data,
                headers=headers,
                files=files,
                )
            if u.status_code==201:
                logerror("        upload correcto archivo {}".format(f[0].name))
            else:
                logerror("        error upload archivo {} mensaje: {}".format(
                    f[0].name,
                    u.text))
        else:
            logerror("        cuil no encontrado " + file)

    o = requests.get(
        apiUrl + "/logout"
        )
    logerror("Fin del proceso")


if __name__ == "__main__":
    main(argv[1:])
