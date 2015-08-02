from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import IntegrityError
from learninground import settings
from registration.models import RegistrationProfile

def create_user(email, role):
    username = email.split('@')[0]
    print 'u: %s' % username
    
    try:
        user = User.objects.create_user(username, email)
        site = Site.objects.get(id=settings.SITE_ID)
        RegistrationProfile.objects.create_inactive_user(site=site, new_user=user)
        # set attributes based on other fields ('role', etc)
    except IntegrityError:
        pass
        # Inform user username is already taken

def create_guardian(user, guardian_email):
    username = guardian_email.split('@')[0]
    print 'g: %s' % username

    # create user for parent
    # create association for student-parent
