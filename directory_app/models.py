
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models




SUBJECT_CHOICES = (
    (False, 'None'),
    ('english', 'English - Reading'),
    ('math', 'Math'),
    ('science', 'Science'),
    ('socStud', 'Social Studies'),
    ('specialEd', 'Special Education'),
    ('language', 'Language Studies'),
    ('techCareer', 'Technology and Career Applications'),
)


SCHOOL_CHOICES = (
    (False, 'None'),
    ('LES', 'Lillian Elementary'),
    ('AES', 'Elementary South'),
    ('AEN', 'Elementary North'),
    ('AIS', 'Intermediate'),
    ('AJH', 'Junior High'),
    ('AHS', 'High School'),
    ('Administration', 'Administration'),
    ('Operations', 'Operations'),
    ('Special Services', 'Special Services'),
    ('Technology', 'Technology'),
)

ADD_TYPE_CHOICES = (
    ('district', 'District'),
    ('targeted', 'Targeted'),
    ('tutorial', 'Tutorial'),
    ('tool', 'Tool'),
)

class UserInfo(models.Model):
    school = models.CharField(max_length=45, verbose_name='school', blank=True, null=True)
    google_id = models.CharField(max_length=65, verbose_name='Google ID', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='username', blank=True, null=True)
    lastName = models.CharField(max_length=45, verbose_name='Last Name', blank=True, null=True)
    firstName = models.CharField(max_length=45, verbose_name='First Name', blank=True, null=True)
    email = models.EmailField(max_length=80, blank=True, null=True)
    grade = models.CharField(max_length=45, verbose_name='Grade', blank=True, null=True)
    job = models.CharField(max_length=85, verbose_name='Occupation', blank=True, null=True)
    subject = models.CharField(max_length=45, blank=True, null=True)
    roomNumber = models.CharField(max_length=8, blank=True, null=True)
    phoneExtension = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.lastName, self.firstName)
    
    class Meta:
        ordering = ['lastName', 'firstName']
        
        
class UserAdmin(models.Model):
    email = models.EmailField(max_length=80, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.email)
    