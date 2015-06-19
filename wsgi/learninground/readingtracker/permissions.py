from default.models import Friendship
from rest_framework import permissions

class IsOwnerOrFriend(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        has_permission = False

        # Perhaps encapsulate this in an is_friend method somewhere
        friendship = Friendship.objects.filter(user=user, friend=obj.user, active=True)

        if friendship:
            if request.method in permissions.SAFE_METHODS:
                has_permission = True

        if obj.user == user:
            has_permission = True

        print has_permission

        return has_permission
