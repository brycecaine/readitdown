from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^reading/?', include('readingtracker.urls', namespace='readingtracker')),
    url(r'^access/?', include('access.urls', namespace='access')),
    url(r'^', include('main.urls', namespace='main')),
)
