from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.db import IntegrityError
from readitdown import settings
from registration.models import RegistrationProfile

def create_user(email, first_name=None, last_name=None, group_name=None):
    print email
    print User.objects.all()
    username = email.split('@')[0]
    
    try:
        user = User.objects.create_user(username, email)
        print user
        print 1
        user.first_name = first_name
        print 1.1
        user.last_name = last_name
        print 1.2
        # Figure out why this user.save() is creating an exception
        user.save()

        print 2
        group = Group.objects.get(name=group_name) 
        group.user_set.add(user)
        print 3
        site = Site.objects.get(id=settings.SITE_ID)
        RegistrationProfile.objects.create_inactive_user(site=site, new_user=user)
        print 4

    except IntegrityError:
        print 'user %s exists' % username
        print 5
        user = None

    return user

def is_manager(user):
    return user.groups.filter(name='manager').exists()

def is_teacher(user):
    return user.groups.filter(name='teacher').exists()
