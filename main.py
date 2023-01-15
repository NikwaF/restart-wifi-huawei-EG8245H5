from router import LoginPage

def main():
    loginPage = LoginPage()
    loginPage.login_request()
    loginPage.get_onttoken()
    loginPage.restart_router()

if (__name__ == "main"):
    main()