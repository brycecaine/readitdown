from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.db import IntegrityError
from main import service as main_service
from main.models import Friendship, Profile
from readitdown import settings
from registration.models import RegistrationProfile
import csv
import random
import string
import xlrd

def provision_user(email, group_name, school, first_name=None, last_name=None, **extras):
    username = email.split('@')[0]
    
    try:
        new_user = User.objects.create_user(username, email)
        if first_name:
            new_user.first_name = first_name
        if last_name:
            new_user.last_name = last_name
        if first_name or last_name:
            new_user.save()

        site = Site.objects.get(id=settings.SITE_ID)

        RegistrationProfile.objects.create_inactive_user(site=site, new_user=new_user)
        last_six = new_user.registrationprofile.activation_key[-6:]
        password = '%s%s' % (username, last_six)
        new_user.set_password(password)
        new_user.save()

        group = Group.objects.get(name=group_name) 
        group.user_set.add(new_user)

        profile = Profile.objects.create(user=new_user, school=school)

    except IntegrityError:
        new_user = User.objects.get(username=username)

    return new_user

def is_manager(user):
    return user.groups.filter(name='manager').exists()

def is_teacher(user):
    return user.groups.filter(name='teacher').exists()

def import_users(file, user, group_to_assign):
    message = 'Import failed'

    school = user.profile.school

    dict_list = get_dict_list(file)

    for file_dict in dict_list:
        file_dict['group_name'] = group_to_assign
        file_dict['school'] = school
        new_user = provision_user(**file_dict)

        for key, value in file_dict.items():
            if 'guardian' in key:
                guardian_dict = {'email': value, 'group_name': 'guardian', 'school': school}
                guardian = provision_user(**guardian_dict)
                main_service.create_friendship(new_user, guardian, True, 'guardian')

        if is_teacher(user):
            assign_teachership(new_user, user)

    file.close()

    message = 'Import successful'

    return message

def assign_teachership(user, teacher):
    # Deactivate old teacher friendships
    old_teacher_friendships = Friendship.objects.filter(user=user, active=True, friend_type='teacher')
    for old_teacher_friendship in old_teacher_friendships:
        old_teacher_friendship.active = False
        old_teacher_friendship.save()

    # Create the new teacher friendship
    friendship = main_service.create_friendship(user, teacher, True, 'teacher')

    return friendship

def get_dict_list(file):
    content_type = file.content_type

    # Handle CSVs
    if content_type == 'text/csv':
        dict_list = csv.DictReader(file)

    # Handle Excel files
    elif content_type in ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'):
        workbook = xlrd.open_workbook(filename=None, file_contents=file.read())
        sheet = workbook.sheet_by_index(0)
        headings = sheet.row_values(1)
        dict_list = []

        for rownum in range(sheet.nrows)[2:]:
            row = sheet.row_values(rownum)
            row_dict = {}

            for i, item in enumerate(row):
                row_dict[headings[i]] = item

            dict_list.append(row_dict)

    return dict_list
