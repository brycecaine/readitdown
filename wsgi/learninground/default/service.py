from default.models import Friendship
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.db import IntegrityError
from learninground import settings
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

def create_friendship(user, friend, active, friend_type):
    friendship = None
    if friend:
        friendship, created = Friendship.objects.get_or_create(user=user,
            friend=friend, friend_type=friend_type, active=True)

    return friendship

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()
