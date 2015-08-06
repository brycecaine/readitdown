from django.contrib.auth.models import User
from django.db import models

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friends_to')
    friend = models.ForeignKey(User, related_name='friends_from')
    friend_type = models.CharField(max_length=100, blank=True, null=True)
    active = models.NullBooleanField()

    def __unicode__(self):
        return '%s & %s - %s, %s' % (self.user, self.friend, self.friend_type, self.active)
