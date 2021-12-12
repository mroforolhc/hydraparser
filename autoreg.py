from datetime import datetime

from torSession import TorSession
from storage import Storage
from hydra import Hydra
from utils import getRandomString

def getIpAddress(session):
    return session.get('http://httpbin.org/ip').json()['origin']

store = Storage('data.csv')
session = TorSession()

currentIp = getIpAddress(session)
print('Текущий ip: ', currentIp)
print('Количество записей в файле: ', len(store.data))


site = Hydra(session)

isReg = False
while not isReg:
    login = getRandomString()
    name = getRandomString()
    password = getRandomString()

    print(login, name, password)

    isReg = site.registration(login, name, password)

btcWallet = site.getWallet()
promocode = site.getPromo()

store.append({
    'id': len(store.data) + 1,
    'login': login,
    'name': name,
    'password': password,
    'ip': currentIp,
    'btcWallet': btcWallet,
    'promocode': promocode,
    'date': datetime.now().strftime("%d.%m.%Y %H:%M:%S")
})