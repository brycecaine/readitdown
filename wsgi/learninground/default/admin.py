from default.models import Friendship, Term, Course, Section, UserSection
from django.contrib import admin

class FriendshipAdmin(admin.ModelAdmin):
    pass

admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserSection)
