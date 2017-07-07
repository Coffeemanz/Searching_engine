from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [    
	url(r'^$', 'searching_engine.views.home', name='home'),
	url(r'^request', 'searching_engine.views.req', name='home'),
]
