from django.contrib.auth.models import User
from django.db import models

class Term(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.start_date, self.end_date)

class Course(models.Model):
    # Like CHEM 101 or first grade
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    course_number = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.subject, self.course_number)

class Section(models.Model):
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    teacher = models.ForeignKey(User)
    section_number = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s %s %s' % (self.course, self.term, self.section_number)

class UserSection(models.Model):
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section)

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='users')
    friend = models.ForeignKey(User, related_name='friends')
    active = models.NullBooleanField()
    is_parent = models.NullBooleanField()
