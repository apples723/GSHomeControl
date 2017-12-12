import time
import requests
from collections import OrderedDict
import json

def GetToken():
	param = OrderedDict([("appType", "Kasa_Android"), ("cloudUserName","gmsiders@gmail.com"),("cloudPassword","Samdobgs1!"),("terminalUUID","bc6b4f18-51af-44f1-b071-5fb450f4ca7a")])
	data = json.dumps(OrderedDict([("method", "login") , ("params", param)]))
	r = requests.post('https://wap.tplinkcloud.com', data=data)
	token_data = json.loads(r.text)
	token = token_data['result']['token']
	return token


#Turns specific light off
def TONHL(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"set_relay_state\":{\"state\":1}}}" )])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token }
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	print(r.text)


#Turns specific light on
def TOFFHL(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"set_relay_state\":{\"state\":0}}}" )])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token }
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	print(r.text)


#####Morse code ######
CODE = {' ': ' ',
        "'": '.----.',
        '(': '-.--.-',
        ')': '-.--.-',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.-.-',
        '/': '-..-.',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ':': '---...',
        ';': '-.-.-.',
        '?': '..--..',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '_': '..--.-'}
######End of morse code######
token = GetToken()

def dot():
        TONHL(token,'800672725445CE0D42A27102C4DD6CEE18A62247')
        time.sleep(0.2)
        TOFFHL(token,'800672725445CE0D42A27102C4DD6CEE18A62247')
        time.sleep(0.2)

def dash():
        TONHL(token,'800672725445CE0D42A27102C4DD6CEE18A62247')
        time.sleep(0.5)
        TOFFHL(token,'800672725445CE0D42A27102C4DD6CEE18A62247')
        time.sleep(0.2)

input = "merry christmas"
for letter in input:
        for symbol in CODE[letter.upper()]:
                if symbol == '-':
                        dash()
                elif symbol == '.':
                        dot()
                else:
                        time.sleep(0.5)
        time.sleep(0.5)


