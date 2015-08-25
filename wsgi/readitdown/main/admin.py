from main.models import Friendship
from django.contrib import admin

class FriendshipAdmin(admin.ModelAdmin):
    pass

admin.site.register(Friendship, FriendshipAdmin)
