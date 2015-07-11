from calendar import monthrange
from datetime import date, datetime
from default.models import Section
from django.contrib.auth.models import User
from readingtracker.models import Entry
import time

def get_entry_data(username):
    user = User.objects.get(username=username)
    entries = Entry.objects.filter(user=user)

    entry_data = []
    for entry in entries:
        entry_date = entry.date.strftime('%m/%d/%y')

        entry_dict = {
            'date': entry_date,
            'minutes': entry.minutes,
            'pages': entry.pages
        }

        entry_data.append(entry_dict)

    return entry_data

def get_sections(username):
    user = User.objects.get(username=username)
    sections = Section.objects.filter(teacher=user)

    return sections

def get_section_entries(section, year, month):
    # Get date range
    days = range(1, monthrange(year, month)[1] + 1)
    date_list = []
    columns = [{'title': 'Name'}]
    for day in days:
        date_list.append(date(year, month, day))
        columns.append({'title': day})

    students = get_students(section)
    data = []
    for student in students:
        student_data = [student.username]
        for entry_date in date_list:
            try:
                entry = Entry.objects.get(user=student, date=entry_date)
                student_data.append(entry.minutes)
            except Entry.DoesNotExist:
                student_data.append(0)
        data.append(student_data)

    return {'columns': columns, 'data': data}

def get_students(section):
    students = User.objects.filter(usersection__section=section)

    return students
