from django.contrib import admin
from default.models import Friendship
from readingtracker.models import Entry

class FriendshipAdmin(admin.ModelAdmin):
    pass
class EntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Entry, EntryAdmin)
