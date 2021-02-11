import requests


def main():
        r = requests.post(
            "https://rockuapp.com/login/",
            data={
                'email': 'rooftop@rocku.com',
                'password': 'admin'},
            headers={
                "Content-Type": "application/x-www-form-urlencoded"}
            )

        f = open('20-29087702-5_20210208_0_711521050.pdf', 'rb'),

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

        data = {
            "employeeId": "395",
            "name": "Recibo",
            "MAX_FILE_SIZE": "2000000",
            }

        x = requests.post(
            'https://rooftop.rockuapp.com/documents/',
            data=data,
            headers=headers,
            files=files,
            )


if __name__ == "__main__":
    main()
