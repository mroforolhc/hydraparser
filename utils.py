import base64
import random

def saveCaptcha(path, data):
    data_img = data.replace('data:image/jpeg;base64,', '').encode('utf-8')

    with open(path, 'wb') as f:
        f.write(base64.decodebytes(data_img))

def getRandomString(l = 15): 
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(alphabet[random.randint(0, len(alphabet) - 1)] for i in range(l)) 