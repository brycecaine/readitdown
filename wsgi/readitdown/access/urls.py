from access.decorators import require_groups
from django.conf.urls import patterns, url
from access import views

urlpatterns = patterns('',
    url(r'^addusers/?$', require_groups('manager', 'teacher')
        (views.AddUsersView.as_view()), name='addusers'),
)


