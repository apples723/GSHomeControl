import requests
import json
from collections import OrderedDict

def GetToken():
	s = requests.Session()
	s.get('https://my.meethue.com/en-us/?token=ca11b7e83e8cb6b83bea8f1482168faf7ed92aaf123f753f899b3ec99b3409cb291b97d961a419be07c9ace1e77069e076841297c7bf0a9e7f81904e54581cbe')
	cookies = s.cookies.get_dict()
	token = cookies['myhueapi']
	return token

def GetHeaders():
	token = GetToken()
	headers = OrderedDict([("x-token",token),("content-type","application/json")])
	return headers


def GetStatus(header):
	header = header
	r = requests.get("https://client.meethue.com/api/0", headers=header)
	return r.text
	

def GetBulbStatus(status, bulbid):
	status = json.loads(status)
	id = bulbid
	state = status['lights'][id]['state']['on']
	if state == True:
		print("Light is on")
	if state == False:
		print("Light is off")

 
	
	