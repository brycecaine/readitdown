from django.conf.urls import patterns, include, url
from django.contrib import admin
from default import views

urlpatterns = patterns('',
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^reading/?', include('readingtracker.urls', namespace='readingtracker')),
    url(r'^', views.HomeView.as_view(), name='home'),
)
