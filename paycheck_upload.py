import requests
from getopt import getopt, GetoptError
from sys import argv, exit
import pyexcel as pe
from os import listdir, path, makedirs


def getHelp():
    print(
        'INSTRUCTIONS\n \n' +
        '============\n \n' +
        'First you need to install requirements: \n' +
        '   pip install -r requirements.txt \n \n' +
        '   All the files in filesDir must be PDF.\n \n' +
        'Command Example: \n' +
        '   python paycheck_upload.py' +
        ' -a <apiUrl> -d <documentsUrl> -u <username> -p <password> -f <filesDir>\n'
        '   ================================================== \n' +
        '   =          All Parameters are requiered          = \n' +
        '   ================================================== \n \n'
        )


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
        print("\n The Parameters are not optionals !!!")
        print("\n ====================================")
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
            print(f + " is not a \'PDF\' file.")
    if flag:
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

    for file in files:
        # f = open(path_to_files + '20-29087702-5_20210208_0_711521050.pdf', 'rb'),
        f = open(path_to_files + file, 'rb'),

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

        # ToDo: This must be dinamic, based on cuil in file name
        data = {
            "employeeId": "395",
            "name": "Recibo",  # fixed
            "MAX_FILE_SIZE": "2000000",  # fixed
            }

        u = requests.post(
            documentsUrl,
            data=data,
            headers=headers,
            files=files,
            )

    o = request.get(
        apiUrl + "/logout"
        )


if __name__ == "__main__":
    main(argv[1:])
