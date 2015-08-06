from django.conf.urls import patterns, url
from readingtracker import views

urlpatterns = patterns('',
    url(r'^monitor/?$', views.MonitorView.as_view(), name='readingmonitor'),
    url(r'^$', views.HomeView.as_view(), name='readingtracker'),
)

