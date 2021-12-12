import time
from bs4 import BeautifulSoup as Soup

from utils import saveCaptcha

class Hydra:
    url = 'http://hydraclubbioknikokex7njhwuahc2l67lfiz7z36md2jvopda7nchid.onion'

    def __init__(self, session) -> None:
        self.session = session
        self.getAccess()

    def getErrors(self, soup):
        errors = []
        alert = soup.select('.log_page .alert-danger')
        if (alert):
            for error in alert[0]:
                clearError = error.get_text().replace('×', '').strip()
                if (clearError):
                    errors.append(clearError)
        
        return errors

    def logout(self):
        print('Выходим из аккаунта...')
        r = self.session.get(self.url)
        soup = Soup(r.text, 'html.parser')

        logoutLink = soup.select_one('.user_head .dropdown-menu li:last-child a').get('href')
        self.session.get(self.url + logoutLink)

    def getAccess(self) -> None:
        firstConnect = True

        print('Проходим защитную капчу...')
        r = self.session.get(self.url)
        
        while True:         
            soup = Soup(r.text, 'html.parser')

            if soup.title.contents[0] != 'Вы не робот?':
                break
            elif not firstConnect:
                print('Капча неправильная')

            saveCaptcha('startCaptcha.jpg', soup.form.img.get('src'))
            
            captchaData = soup.form.find('input', attrs={'name': 'captchaData'}).get('value')
            captcha = input('Капча загружена. Введите её: ')
            r = self.session.post(self.url + '/gate', data = {
                'captchaData': captchaData,
                'captcha': captcha,
                'ret': '/',
            })

            firstConnect = False
    
    def registration(self, login, name, password):
        invalidParams = False
        print('Регистрируемся...')
        
        r = self.session.get(self.url + '/register')

        while r.url == self.url + '/register':
            soup = Soup(r.text, 'html.parser')
            errors = self.getErrors(soup)

            for error in errors:
                print(error)
                if (error != 'Вы ввели неверный код с картинки') and \
                    (error != 'Капча устарела (срок действия 3 мин)'):
                    invalidParams = True

            if (invalidParams):
                time.sleep(1)
                break
            
            saveCaptcha('registerCaptcha.png', soup.form.img.get('src'))
            captchaData = soup.form.find('input', attrs={'name': 'captchaData'}).get('value')

            captcha = input('Введите капчу для регистрации: ')
            r = self.session.post(self.url + '/register', data = {
                'captchaData': captchaData,
                'captcha': captcha,
                'code': 'bp3000',
                'auth_login': login,
                'login': name,
                'password': password,
                'password_confirmation': password,
                '_token': '',
            })

        if (invalidParams):
            return False

        print('Принимаем условия соглашения...')

        soup = Soup(r.text, 'html.parser')
        form = soup.find('form', attrs={'action': '/info/rules/accept'})
        
        r = self.session.post(self.url + '/info/rules/accept', data = {
            '_token': form.find('input', attrs={'name': '_token'}).get('value'),
            'rules_id': form.find('input', attrs={'name': 'rules_id'}).get('value'),
        })

        print('Выбираем страну...')

        soup = Soup(r.text, 'html.parser')
        form = soup.find('form', attrs={'action': '/set-country'})
        
        r = self.session.post(self.url + '/set-country', data = {
            '_token': form.find('input', attrs={'name': '_token'}).get('value'),
            'region_id[1]': '',
            'country_id': 2,
            'region_id[2]': 155,
            'region_id[3]': '',
            'region_id[4]': '',
            'region_id[5]': '',
            'region_id[6]': '',
            'region_id[8]': '',
            'region_id[9]': '',
            'region_id[10]': '',
            'region_id[11]': '',
            'remember': 1,
        })

        if (r.url != self.url):
            return False

        return True

    def auth(self, login, password):
        invalidParams = False
        print('Авторизуемся...')
        r = self.session.get(self.url + '/login')

        while r.url == self.url + '/login':
            soup = Soup(r.text, 'html.parser')
            errors = self.getErrors(soup)

            for error in errors:
                print(error)
                if (error != 'Вы ввели неверный код с картинки') and \
                    (error != 'Капча устарела (срок действия 3 мин)'):
                    invalidParams = True

            if (invalidParams):
                time.sleep(1)
                break
            
            saveCaptcha('loginCaptcha.png', soup.form.img.get('src'))
            captchaData = soup.form.find('input', attrs={'name': 'captchaData'}).get('value')

            captcha = input('Введите капчу для авторизации: ')
            r = self.session.post(self.url + '/login', data = {
                'captchaData': captchaData,
                'captcha': captcha,
                'login': login,
                'password': password,
                '_token': '',
                'redirect': 1,
            })

        time.sleep(1)
    
        if (invalidParams):
            return False

        print('Вход выполнен')

        return True


    def getWallet(self):
        print('Сохраняем кошелёк...')

        r = self.session.get(self.url + '/balance')
        soup = Soup(r.text, 'html.parser')
        btcAddress = soup.select_one('.balance_list li:nth-child(2) .panel').get_text().strip()
        
        return btcAddress

    def getPromo(self):
        print('Сохраняем промокод...')

        r = self.session.get(self.url + '/discounts/history')
        soup = Soup(r.text, 'html.parser')
        code = soup.tbody.tr.select_one('td:nth-child(3)').get_text()

        return code
