from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'learninground.views.home', name='lr_home'),
    url(r'^readingtracker/?$', 'readingtracker.views.home', name='rt_home'),
    url(r'^admin/', include(admin.site.urls)),
)
