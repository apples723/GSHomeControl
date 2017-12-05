from django.shortcuts import render
from django.views.generic import TemplateView
from collections import OrderedDict
import json
import requests
####SMART HOME API STUFF#####

#So my password for my account is not on github...
PassDoc = open("../../password.txt", 'r')
Password = PassDoc.read()

#KASA HOME STUFF##
def GetToken():
	param = OrderedDict([("appType", "Kasa_Android"), ("cloudUserName","gmsiders@gmail.com"),("cloudPassword", Password),("terminalUUID","c55f1c98-f486-4a69-8ce6-adb9ce6f0eea")])
	data = json.dumps(OrderedDict([("method", "login") , ("params", param)]))
	r = requests.post('https://wap.tplinkcloud.com', data=data)
	token_data = json.loads(r.text)
	token = token_data['result']['token']
	return token
	
def GetKasaDeviceStatus(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"get_sysinfo\":{}}}")])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token } 
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	device_status = json.loads(r.text)
	status = json.loads(device_status['result']['responseData'])['system']['get_sysinfo']['relay_state']
	if status == 1:
		return "on"
	if status == 0:
		return "off"

def GetKasaDeviceList(token):
	data = { "method" : "getDeviceList" }
	param = {"token" : token }
	r = requests.post('https://wap.tplinkcloud.com', params=param, data=json.dumps(data))
	device_list = json.loads(r.text)
	devices = []
	for i in device_list['result']['deviceList']:
		alias = i['alias']
		id = i['deviceId']
		devices.append([alias,id])
	return devices
			
def TurnOnSmartPlug(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"set_relay_state\":{\"state\":1}}}" )])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token }
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	print(r.text)

def TurnOffSmartPlug(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"set_relay_state\":{\"state\":0}}}" )])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token }
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	print(r.text)

##HUE STUFF##

""" IN DEVELOPMENT 

def GetHueToken():
	s = requests.Session()
	s.get('https://my.meethue.com/en-us/?token=ca11b7e83e8cb6b83bea8f1482168faf7ed92aaf123f753f899b3ec99b3409cb291b97d961a419be07c9ace1e77069e076841297c7bf0a9e7f81904e54581cbe')
	cookies = s.cookies.get_dict()
	HueToken = cookies['myhueapi']
	return HueToken
def GetStatus(token):
	
"""
#Begin Django View###
def HomePageStrings():
	token = GetToken()
	devices = GetKasaDeviceList(token)
	data = OrderedDict([('token', token), ('devices', devices)])
	return data
def dashboard(request):
	data = HomePageStrings()
	token = data['token']
	id1 = data['devices'][0][1]
	id2 = data['devices'][1][1]
	name1 = data['devices'][0][0]
	name2 = data['devices'][1][0]
	status1 = GetKasaDeviceStatus(token, id1)
	status2 = GetKasaDeviceStatus(token, id2)
	return render(request, 'index.html', {'id1': id1, 'status1': status1, 'name1': name1,'id2': id2, 'status2': status2, 'name2': name2})
	
	
def turnoff(request):
	token = GetToken()
	id = request.GET.get('id')
	TurnOffSmartPlug(token,id)
	data = HomePageStrings()
	token = data['token']
	id1 = data['devices'][0][1]
	id2 = data['devices'][1][1]
	name1 = data['devices'][0][0]
	name2 = data['devices'][1][0]
	status1 = GetKasaDeviceStatus(token, id1)
	status2 = GetKasaDeviceStatus(token, id2)
	return render(request, 'index.html', {'id1': id1, 'status1': status1, 'name1': name1,'id2': id2, 'status2': status2, 'name2': name2})
	
def turnon(request):
	token = GetToken()
	id = request.GET.get('id')
	TurnOnSmartPlug(token,id)
	data = HomePageStrings()
	token = data['token']
	id1 = data['devices'][0][1]
	id2 = data['devices'][1][1]
	name1 = data['devices'][0][0]
	name2 = data['devices'][1][0]
	status1 = GetKasaDeviceStatus(token, id1)
	status2 = GetKasaDeviceStatus(token, id2)
	return render(request, 'index.html', {'id1': id1, 'status1': status1, 'name1': name1,'id2': id2, 'status2': status2, 'name2': name2})
	