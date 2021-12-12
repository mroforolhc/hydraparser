from torSession import TorSession
from storage import Storage
from hydra import Hydra

accounts = Storage('data.csv')
checkedAccounts = Storage('checkedAccounts.csv')

session = TorSession()
site = Hydra(session)

for index, account in enumerate(accounts.data):
    print('\nПроверка аккаунта №' + str(index + 1))
    isAuth = site.auth(account['login'], account['password'])

    if (isAuth):
        checkedAccounts.append(account)
        site.logout()