from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from main.models import Friendship
from readingtracker import service
from readingtracker.forms import EntryForm
from readingtracker.models import Entry
import csv
import json

class HomeView(FormView):
    template_name = 'readingtracker/home.html'
    form_class = EntryForm
    success_url = '/reading'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user

        entry_data = service.get_entry_data(user.username)
        context['entry_data'] = json.dumps(entry_data)

        return context

    def form_valid(self, form):
        # Get form data
        user = self.request.user
        date = form.cleaned_data.get('date')
        minutes = form.cleaned_data.get('minutes')
        pages = form.cleaned_data.get('pages')

        # Create entry

        try:
            entry = Entry.objects.get(user=user, date=date)
            entry.minutes = minutes
            entry.pages = pages
            entry.save()
        except Entry.DoesNotExist:
            entry = Entry.objects.create(user=user, date=date, minutes=minutes, pages=pages)

        return super(HomeView, self).form_valid(form)

class MonitorView(TemplateView):
    template_name = 'readingtracker/monitor.html'

    def get_context_data(self, **kwargs):
        context = super(MonitorView, self).get_context_data(**kwargs)
        user = self.request.user
        year = int(self.kwargs.get('year', datetime.now().year))
        month = int(self.kwargs.get('month', datetime.now().month))

        ref_date = date(year, month, 1)
        period = ref_date.strftime('%B')

        next_month_date = ref_date + relativedelta(months=1)
        next_month_month = next_month_date.month
        next_month_year = next_month_date.year

        prev_month_date = ref_date + relativedelta(months=-1)
        prev_month_month = prev_month_date.month
        prev_month_year = prev_month_date.year

        table_data = service.get_friend_entries(user, 'teacher', year, month)

        context['columns'] = json.dumps(table_data['columns'])
        context['data'] = json.dumps(table_data['data'])
        context['period'] = '%s %s' % (period, year)
        context['prev_month_month'] = prev_month_month
        context['prev_month_year'] = prev_month_year
        context['month'] = month
        context['year'] = year
        context['next_month_month'] = next_month_month
        context['next_month_year'] = next_month_year

        return context

class FriendEntriesJSONView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        year = int(self.kwargs.get('year', datetime.now().year))
        month = int(self.kwargs.get('month', datetime.now().month))

        table_data = service.get_friend_entries(user, 'teacher', year, month)

        data = {'data': table_data}

        return JsonResponse(data)

class FriendEntriesCSVView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        year = int(self.kwargs.get('year', datetime.now().year))
        month = int(self.kwargs.get('month', datetime.now().month))

        table_data = service.get_friend_entries(user, 'teacher', year, month)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="list_%s_%s.csv"' % (year, month)

        writer = csv.writer(response)
        columns = [d['title'] for d in table_data['columns']]
        writer.writerow(columns)
        for row in table_data['data']:
            writer.writerow(row)

        return response
