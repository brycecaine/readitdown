from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.views.generic.base import TemplateView
from default.models import Friendship
from readingtracker.models import Entry
from readingtracker.permissions import IsOwnerOrFriend
from readingtracker.serializers import UserSerializer, GroupSerializer, EntrySerializer
from rest_framework import viewsets, permissions, filters

class IsOwnerOrFriendFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        friend_ids = Friendship.objects.filter(user=user, active=True).values_list('friend__id', flat=True)
        q_user_or_friend = Q(user=user) | Q(user__id__in=friend_ids)
        qs = queryset.filter(q_user_or_friend)
        return qs

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (IsOwnerOrFriendFilterBackend,)
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrFriend
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HomeView(TemplateView):

    template_name = 'readingtracker/home.html'
