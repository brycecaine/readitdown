from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.views.generic.edit import FormView
from default.models import Friendship
from readingtracker import service
from readingtracker.forms import EntryForm
from readingtracker.models import Entry
from readingtracker.permissions import IsOwnerOrFriend
from rest_framework import viewsets, permissions, filters
import json

class IsOwnerOrFriendFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        friend_ids = Friendship.objects.filter(user=user, active=True).values_list('friend__id', flat=True)
        q_user_or_friend = Q(user=user) | Q(user__id__in=friend_ids)
        qs = queryset.filter(q_user_or_friend)
        return qs

class HomeView(FormView):
    template_name = 'readingtracker/home.html'
    form_class = EntryForm
    success_url = '/reading'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user

        entry_data = service.get_entry_data(user.username)
        print entry_data
        context['entry_data'] = json.dumps(entry_data)

        return context

    def form_valid(self, form):
        # Get form data
        user = self.request.user
        date = form.cleaned_data.get('date')
        minutes = form.cleaned_data.get('minutes')
        pages = form.cleaned_data.get('pages')

        # Create entry
        entry = Entry.objects.create(user=user, date=date, minutes=minutes, pages=pages)

        return super(HomeView, self).form_valid(form)
