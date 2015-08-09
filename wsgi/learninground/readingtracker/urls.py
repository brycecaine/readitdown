from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from readingtracker import views

urlpatterns = patterns('',
    url(r'^monitor/?$', login_required(views.MonitorView.as_view()), name='readingmonitor'),
    url(r'^monitor/(?P<year>\d+)/(?P<month>\d+)/?$', login_required(views.MonitorView.as_view()), name='readingmonitor'),
    url(r'^$', login_required(views.HomeView.as_view()), name='readingtracker'),
)

