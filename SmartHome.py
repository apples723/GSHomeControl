import requests, json 
from collections import OrderedDict

#http://itnerd.space/2017/05/21/how-to-get-the-tp-link-hs100-cloud-end-point-url/
#http://itnerd.space/2017/01/22/how-to-control-your-tp-link-hs100-smartplug-from-internet/


def GetToken():
	param = OrderedDict([("appType", "Kasa_Android"), ("cloudUserName","gmsiders@gmail.com"),("cloudPassword","***!"),("terminalUUID","bc6b4f18-51af-44f1-b071-5fb450f4ca7a")])
	data = json.dumps(OrderedDict([("method", "login") , ("params", param)]))
	r = requests.post('https://wap.tplinkcloud.com', data=data)
	token_data = json.loads(r.text)
	token = token_data['result']['token']
	return token


def GetKasaDeviceList(token):
	data = { "method" : "getDeviceList" }
	param = {"token" : token }
	r = requests.post('https://wap.tplinkcloud.com', params=param, data=json.dumps(data))
	device_list = json.loads(r.text)
	ID = []
	for i in device_list['result']['deviceList']:
		ID.append(i['deviceId'])
	return ID


def TurnOnSmartPlug(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"set_relay_state\":{\"state\":1}}}" )])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token }
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	print r.text

def TurnOffSmartPlug(token,id):
	params = OrderedDict([("deviceId", id), ("requestData", "{\"system\":{\"set_relay_state\":{\"state\":0}}}" )])
	data = json.dumps(OrderedDict([("method", "passthrough") , ("params", params)]))
	param = {"token" : token }
	r = requests.post('https://use1-wap.tplinkcloud.com/', params=param, data=data)
	print r.text
	
	
##Testing

token = GetToken()
DeviceList = GetKasaDeviceList(token)
ID = DeviceList[0]
TurnOnSmartPlug(token,ID)

