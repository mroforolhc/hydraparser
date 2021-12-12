import requests

class TorSession:
    def __init__(self):
        self.headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0', 
        }

        session = requests.session()
        session.proxies = {
            'http':  'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050',
        }

        self.session = session
    
    def get(self, url):
        return self.session.get(url, headers=self.headers)

    def post(self, url, data):
        return self.session.post(url, headers=self.headers, data=data)