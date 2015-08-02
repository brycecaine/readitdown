from django.conf.urls import patterns, include, url
from django.contrib import admin
from default import views

urlpatterns = patterns('',
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^reading/?', include('readingtracker.urls', namespace='readingtracker')),
    url(r'^addusers/?', include('default.urls', namespace='default')),
    url(r'^', views.HomeView.as_view(), name='home'),
)
