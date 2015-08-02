from default.models import Friendship
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import IntegrityError
from learninground import settings
from registration.models import RegistrationProfile

def create_user(email, role, related_user=None):
    print email
    username = email.split('@')[0]
    
    try:
        user = User.objects.create_user(username, email)
        print user
        site = Site.objects.get(id=settings.SITE_ID)
        RegistrationProfile.objects.create_inactive_user(site=site, new_user=user)
        # TODO set attributes based on other fields ('role', etc)

        # Create friendship for student-guardian
        if related_user:
            friendship = Friendship.objects.get_or_create(user=related_user, friend=user, active=True, is_parent=True)

        status = 'success'

    except IntegrityError:
        user = None

    return user
