import ast
import requests 
import re
from bs4 import BeautifulSoup
from util import encrypt_base4 

class LoginPage:
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'http://192.168.18.1',
        'Referer': 'http://192.168.18.1/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    def __init__(self) -> None:
        self.hw_token_loginpage = self.get_hwtoken_loginpage()

    def get_hwtoken_loginpage(self) -> str:
        req = requests.post("http://192.168.18.1/asp/GetRandCount.asp", headers=self.headers)
        req.encoding = req.apparent_encoding
        return req.text

    def get_onttoken(self) -> None: 
        r = requests.get('http://192.168.18.1/index.asp', headers=self.headers,cookies=self.cookie, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        self.onttoken = soup.find(id="onttoken").get("value")

    def login_request(self) -> None:
        data = {
            'UserName': 'Epadmin',
            'PassWord': encrypt_base4.base64_to_string('adminEp'),
            'Language': 'english',
            'x.X_HW_Token': self.hw_token_loginpage
        }

        r = requests.post('http://192.168.18.1/login.cgi', headers=self.headers, data=data, verify=False,allow_redirects=False)
        self.cookie = r.cookies
    
    def get_list_dhcp(self) -> None : 
        r = requests.post('http://192.168.18.1/html/bbsp/common/GetLanUserDevInfo.asp', headers=self.headers,cookies=self.cookie, verify=False)
        response = r.text
        matches = re.finditer(r"new USERDevice\(([^)]+)\)", response)

        res = [USERDevice(((match.group(1)).split(","))) for match in matches]
        [print(item) for item in res]

    def restart_router(self) -> None : 
        data = {
            'x.X_HW_Token': self.onttoken,
        }
        try:
            r = requests.post('http://192.168.18.1/html/ssmp/accoutcfg/set.cgi?x=InternetGatewayDevice.X_HW_DEBUG.SMP.DM.ResetBoard&RequestFile=html/ssmp/accoutcfg/ontmngt.asp',data=data, headers=self.headers,cookies=self.cookie, verify=False)
        except requests.exceptions.ConnectionError: 
            print("success restarting the router")
        except: 
            print("error")
        

class USERDevice:
    def __init__(self, element: list[str]) -> None : 
        self.domain = self.eval_escaping(element[0]) 
        self.IpAddress = self.eval_escaping(element[1]) 
        self.MacAddress = self.eval_escaping(element[2]) 
        self.port = self.eval_escaping(element[3]) 
        self.HostName = self.eval_escaping(element[9])

    def __str__(self) -> str:
        return str({"domain": self.domain, "ipAddress": self.IpAddress,"port": self.port,  "macAddress" : self.MacAddress, "hostName": self.HostName})

    def eval_escaping(self, word : str) -> str : 
        string_bytes = word
        string = ast.literal_eval(f"b{string_bytes}").decode()
        return string
