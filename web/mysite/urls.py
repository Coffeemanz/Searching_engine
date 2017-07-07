from django.conf.urls import include, url
from django.contrib import admin
import searching_engine


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('searching_engine.urls')),
    url(r'^request', 'searching_engine.views.req', name='req'), #mb del
    url(r'^indexURL', 'searching_engine.views.indexURL', name='indexURL'),
    url(r'^knownURL', 'searching_engine.views.knownURL', name='knownURL'),
	url(r'^indexWords', 'searching_engine.views.indexWords', name='indexWords'),
]
