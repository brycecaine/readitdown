from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.db import IntegrityError
from main import service as main_service
from main.models import Friendship
from readitdown import settings
from registration.models import RegistrationProfile
import csv
import xlrd

def create_user(email, first_name=None, last_name=None, group_name=None, **extras):
    username = email.split('@')[0]
    
    try:
        user = User.objects.create_user(username, email)
        user.first_name = first_name
        user.last_name = last_name
        # Figure out why this user.save() is creating an exception
        user.save()

        group = Group.objects.get(name=group_name) 
        group.user_set.add(user)

        site = Site.objects.get(id=settings.SITE_ID)
        RegistrationProfile.objects.create_inactive_user(site=site, new_user=user)

    except IntegrityError:
        user = User.objects.get(username=username)

    return user

def is_manager(user):
    return user.groups.filter(name='manager').exists()

def is_teacher(user):
    return user.groups.filter(name='teacher').exists()

def import_users(file, user, group_to_assign):
    message = 'Import failed'

    dict_list = get_dict_list(file)

    for file_dict in dict_list:
        file_dict['group_name'] = group_to_assign
        new_user = create_user(**file_dict)

        for key, value in file_dict.items():
            if 'guardian' in key:
                guardian_dict = {'email': value, 'group_name': 'guardian'}
                guardian = create_user(**guardian_dict)
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
