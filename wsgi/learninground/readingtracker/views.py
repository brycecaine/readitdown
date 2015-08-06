from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from main.models import Friendship
from readingtracker import service
from readingtracker.forms import EntryForm
from readingtracker.models import Entry
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
        table_data = service.get_friend_entries(user, 2015, 7)
        context['columns'] = json.dumps(table_data['columns'])
        context['data'] = json.dumps(table_data['data'])

        return context
