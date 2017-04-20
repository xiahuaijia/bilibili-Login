import requests
import json
import rsa
import binascii
from bs4 import BeautifulSoup
from flask import flash

class fuck_bilibili():
    def __init__(self, username, password = ''):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        self.username = username
        self.password = password
        self.vercode = 0
        self.userData = {}

    def initCookies(self):
        url = 'https://passport.bilibili.com/login'
        self.session.get(url)

    def saveCookies(self, filename = ''):
        filename = "./cookies/%s.cookies" % self.username

        with open(filename, 'w') as f:
            f.write(json.dumps(self.session.cookies.get_dict()))

    def loadCookies(self, filename = ''):
        filename = "./cookies/%s.cookies" % self.username

        try:
            with open(filename, 'r') as f:
                self.session.cookies.update(json.loads(f.read()))
        except:
            return False

        return True

    def getAccountInfo(self):
        url = 'https://account.bilibili.com/home/userInfo'

        try:
            accInfoRes = self.session.get(url)
            soup = BeautifulSoup(accInfoRes.content, 'lxml')
            s = str(soup)
            s = s.replace('<html><body><p>', '')
            s = s.replace('</p></body></html>', '')
            s = s.replace('\n', '')
            s = s.replace('\r', '')
            s = s.replace(' ', '')
            s = s.replace('\t', '')
            self.userData = json.loads(s)
        except:
            return False

        return True

    def isLogin(self):
        if not self.getAccountInfo():
            return False
        if -101 == self.userData['code']:
            return False

        return True

    def getVerCode(self):
        url = 'https://passport.bilibili.com/captcha'
        filename = "./img/%s.jpg" % self.username

        try:
            verCodeRes = self.session.get(url)
            with open(filename, 'wb') as f:
                f.write(verCodeRes.content)
        except:
            return False

        return True

    def rsaEncrypt(self, password):
        url = 'http://passport.bilibili.com/login?act=getkey'

        try:
            getKeyRes = self.session.get(url)
            token = json.loads(getKeyRes.content.decode('utf-8'))
            pw = str(token['hash']+password).encode('utf-8')

            key = token['key']
            key = rsa.PublicKey.load_pkcs1_openssl_pem(key)

            pw = rsa.encrypt(pw, key)
            self.password = binascii.b2a_base64(pw)
        except:
            return False

        return True


    def login(self, vercode):

        url = 'https://passport.bilibili.com/login/dologin'
        data = {
            'act': 'login',
            'gourl': '',
            'keeptime': '2592000',
            'userid': self.username,
            'pwd': self.password,
            'vdcode': vercode
        }

        try:
            loginRes = self.session.post(url=url, data=data)
            soup = BeautifulSoup(loginRes.content, 'lxml')
            s = str(soup.select('center')[0])
            s = s.replace('\n', '')
            s = s.replace('\r', '')
            s = s.replace(' ', '')
            s = s.split('>')
            s = s[2]
            s = s.replace('<br/', '')
            flash(s)
            return False
        except requests.exceptions.ConnectionError as e:
            flash(e)
            return False
        except:
            return True

    def qiandao(self):
        url = 'http://live.bilibili.com/sign/doSign'
        self.session.get(url)