import requests
import json
from collections import OrderedDict


#GET X-TOKEN using AUTH TOKEN FROM HUE USERS ACCOUNT

def GetToken():
	s = requests.Session()
	s.get('https://my.meethue.com/en-us/?token=ca11b7e83e8cb6b83bea8f1482168faf7ed92aaf123f753f899b3ec99b3409cb291b97d961a419be07c9ace1e77069e076841297c7bf0a9e7f81904e54581cbe')
	cookies = s.cookies.get_dict()
	token = cookies['myhueapi']
	return token

#SETS HEADERS FOR REQUEST OBJECT AND GETS TOKEN 
def GetHeaders():
	token = GetToken()
	headers = OrderedDict([("x-token",token),("content-type","application/json")])
	return headers

#RETURNS UNFORMATED JSON OBJECT OF STATUS OF ALL LIGHTS
def GetStatus(header):
	header = header
	r = requests.get("https://client.meethue.com/api/0", headers=header)
	return r.text
	
#GETS LIGHT BULB STATUS OF SPECIFIC BULB
def GetBulbStatus(status, bulbid):
	status = json.loads(status)
	id = bulbid
	state = status['lights'][id]['state']['on']
	if state == True:
		print("Light is on")
	if state == False:
		print("Light is off")

#DATA TYPES ARE IMPORTANT
#>>> json1 = {"on":'true',"bri":'114'}
#>>> json2 = {"on":True,"bri":114}
#>>> j.dumps(json1)
#'{"on": "true", "bri": "114"}'
#>>> j.dumps(json2)
#'{"on": true, "bri": 114}'

#Turns specific light off
def TurnHueLightOff(header, bulbid):
	header = header
	id = bulbid
	data = {"on":False}
	data = json.dumps(data)
	url = "https://client.meethue.com/api/0/lights/%i/state" % id 
	r = requests.put(url,headers=header,data=data)
	result = json.loads(r.text)
	error = 'error' in result[0]
	if error == True:
		result = "Error: Couldn't turn light off"
	if error == False:
		result = "Light succesfully turned on."
	return result
	

#Turns specific light on
def TurnHueLightOn(header, bulbid):
	header = header
	id = bulbid
	data = {"on":True}
	data = json.dumps(data)
	url = "https://client.meethue.com/api/0/lights/%i/state" % id 
	r = requests.put(url,headers=header,data=data)
	result = json.loads(r.text)
	error = 'error' in result[0]
	if error == True:
		result = "Error: Couldn't turn light on"
	if error == False:
		result = "Light succesfully turned on."
	return result
	
#Gets all hue lights status 
def GetAllHueStatus(header):
	status = GetStatus(header)
	status = json.loads(status)
	lights = status['lights']
	AllLightStates = []
	for light in lights:
		id = light
		state = status['lights'][id]['state']['on']
		if state == False:
			state = "off"
		if state == True:
			state = "on"
		bri = status['lights'][id]['state']['bri']
		AllLightStates.append([id,state,bri])
	return AllLightStates

#Set brightness on specific hue light 
def SetHueBrightness(header, bulbid, level):
	id = bulbid
	data = {"bri": level}
	data = json.dumps(data)
	url = "https://client.meethue.com/api/0/lights/%i/state" % id
	r = requests.put(url,headers=header,data=data)
	result = json.loads(r.text)
	error = 'error' in result[0]
	if error == True:
		result = "Error: Light is either off or unreachable."
	if error == False:
		result = "Light brightness succesfully changed."
	return result


	
	

	
