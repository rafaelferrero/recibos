import requests


def login(url, usuario, clave):
    with requests.Session() as s:
        # s.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        s.auth = (usuario, clave)
        r = s.post(url)
        import pdb; pdb.set_trace()


def main():
    loginDomain = "https://rockuapp.com/"
    loginEndpoint = "login/"
    loginUrl = loginDomain + loginEndpoint

    login(loginUrl,
        "rooftop@rocku.com",
        "admin")


if __name__ == "__main__":
    main()
