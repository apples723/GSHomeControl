from django.shortcuts import render
import requests, json 
from collections import OrderedDict
# Create your views here.
#views.py
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from login.forms import RegistrationForm, EditProfileForm
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = {
    'form': form
    }
 
    return render(request, 'registration/register.html' ,variables)
 
def register_success(request):
    return render(request,
    'registration/success.html',)
 
def logout_page(request):
    logout(request)
    return render(request, '/')
"""
def companies(request):
    return render(request,
     'companies.html',)
"""
def currentUsers(request):
    return render(request, 'users.html')

@login_required
def home(request):
    return render(request,
    'home.html',
    { 'user': request.user }
    )


# def currentUsers(request):
#     users_list = Session.objects.filter(expire_date__gte = timezone.now())
#     users_id_list = []
#     for user in users_list:
#         info = user.get_decoded()
#         users_id_list.append(info.get('_auth_user_id', None))
#     context = {users_id_list}

#     return render(request, 'home.html', context)


def view_profile(request):
    args = {'user': request.user}
    return render(request, '/user.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            return redirect('/users')

    else:
        form = EditProfileForm(instance = request.user)
        args = {'form': form}
        return render(request, '/users.html', args)
		

def GetToken():
	param = OrderedDict([("appType", "Kasa_Android"), ("cloudUserName","gmsiders@gmail.com"),("cloudPassword","Samdobgs1!"),("terminalUUID","bc6b4f18-51af-44f1-b071-5fb450f4ca7a")])
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
	if stauts == 0:
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
			
def companies(request):
	token = GetToken()
	devices = GetKasaDeviceList(token)
	id = devices[0][1]
	status = GetKasaDeviceStatus(token, id)
	return render(request, 'companies.html', {'output': status})
	
	

	
	




