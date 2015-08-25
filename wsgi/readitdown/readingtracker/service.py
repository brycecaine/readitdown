from calendar import monthrange
from datetime import date, datetime
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

def get_friend_entries(user, friend_type, year, month):
    # Get date range
    days = range(1, monthrange(year, month)[1] + 1)
    date_list = []
    columns = [{'title': 'Name'}]
    for day in days:
        date_list.append(date(year, month, day))
        columns.append({'title': day, 'width': '2%', 'orderable': False})

    friendships = user.friends_from.filter(friend_type=friend_type, active=True)
    data = []
    for friendship in friendships:
        friend_name = '%s, %s' % (friendship.user.last_name, friendship.user.first_name)
        if friend_name == ', ':
            friend_name = friendship.user.username

        friend_data = [friend_name]
        for entry_date in date_list:
            try:
                entry = Entry.objects.get(user=friendship.user, date=entry_date)
                friend_data.append(entry.minutes)
            except Entry.DoesNotExist:
                friend_data.append(0)
        data.append(friend_data)

    return {'columns': columns, 'data': data}
