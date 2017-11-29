from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.dashboard),
	url(r'^turnoff/$', views.turnoff),
	url(r'^turnon/$', views.turnon),
]