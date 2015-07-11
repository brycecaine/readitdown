from django.conf.urls import patterns, url
from readingtracker import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='readingtracker'),
    url(r'^sections/?$', views.SectionsView.as_view(), name='sections'),
    url(r'^monitor/(?P<section_id>\d+)/?$', views.MonitorView.as_view(), name='readingmonitor'),
)

