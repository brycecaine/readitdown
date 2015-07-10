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
        print entry_date

        entry_dict = {
            'date': entry_date,
            'minutes': entry.minutes,
            'pages': entry.pages
        }

        entry_data.append(entry_dict)

    return entry_data

def get_sections(username):
    user = User.objects.get(username=username)
    sections = Section.objects.filter(user=user)

    return sections
