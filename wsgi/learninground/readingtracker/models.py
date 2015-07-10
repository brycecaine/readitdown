from django.contrib.auth.models import User
from django.db import models

class Entry(models.Model):
    # Add parent_verification later
    user = models.ForeignKey(User)
    date = models.DateTimeField()
    minutes = models.IntegerField()
    pages = models.IntegerField(null=True, blank=True)
    book = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.date, self.minutes, self.pages)
