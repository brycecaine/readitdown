from django.conf.urls import patterns, include, url
from django.contrib import admin
from default.views import HomeView as DHomeView
from readingtracker.views import HomeView as RTHomeView

urlpatterns = patterns('',
    url(r'^$', DHomeView.as_view(), name='lr_home'),
    url(r'^readingtracker/?$', RTHomeView.as_view(), name='rt_home'),
    url(r'^admin/', include(admin.site.urls)),
)
