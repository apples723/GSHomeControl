import requests, json 
from collections import OrderedDict

#http://itnerd.space/2017/05/21/how-to-get-the-tp-link-hs100-cloud-end-point-url/
#http://itnerd.space/2017/01/22/how-to-control-your-tp-link-hs100-smartplug-from-internet/


def GetToken():
	param = OrderedDict([("appType", "Kasa_Android"), ("cloudUserName","gmsiders@gmail.com"),("cloudPassword","********"),("terminalUUID","bc6b4f18-51af-44f1-b071-5fb450f4ca7a")])
	data = json.dumps(OrderedDict([("method", "login") , ("params", param)]))
	r = requests.post('https://wap.tplinkcloud.com', data=data)
	token_data = json.loads(r.text)
	token = token_data['result']['token']
	return token

def TestSetup(TestID):
	if TestID == 1:
		token = GetToken()
		data = { "method" : "getDeviceList" }
		param = {"token" : token }
		r = requests.post('https://wap.tplinkcloud.com', params=param, data=json.dumps(data))
		return r
	else:
		print("No Test Specified")
		
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
	
#1 = on 
#0 = off
#same as binary :)
	
def GetKasaDeviceStatus(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"get_sysinfo\":{}}}")])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token } 
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	device_status = json.loads(r.text)
	status = json.loads(device_status['result']['responseData'])['system']['get_sysinfo']['relay_state']
	if status == 1:
		return "on"
	if stauts == 0:
		return "off"
		
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


	
