from django.conf.urls import patterns, url
from default import views

urlpatterns = patterns('',
    url(r'^$', views.AddUsersView.as_view(), name='addusers'),
)

