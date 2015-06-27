from django.conf.urls import patterns, url
from readingtracker import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='readingtracker'),
)

