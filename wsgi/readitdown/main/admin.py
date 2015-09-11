from main.models import Friendship, School, Profile
from django.contrib import admin

class FriendshipAdmin(admin.ModelAdmin):
    pass

class SchoolAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Profile, ProfileAdmin)
