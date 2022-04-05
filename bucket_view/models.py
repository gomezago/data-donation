from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


# Create your models here.
class Project(models.Model):
    id                      = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    researcher_name         = models.CharField(max_length=200, unique=False, default=None, null=True)
    researcher_affiliation  = models.CharField(max_length=200, unique=False, default=None, null=True)
    title                   = models.CharField(max_length=100, blank=False) # Short string field to hold project name
    description_tweet       = models.CharField(max_length=280, blank=False)  # Tweet-Like description of project
    description             = models.TextField(blank=False)  # Large string frield to hold a piece of text
    hrec                    = models.BooleanField(default=False)
    data                    = models.JSONField(blank=False, null=True)
    data_ext                = models.TextField(blank=True, null=True)
    image                   = models.ImageField(upload_to="images", blank=True, null=True)
    start                   = models.DateField(blank=False)  # Start of project
    end                     = models.DateField(blank=False)  # End of project
    data_info               = models.TextField(blank=False, null=True)
    instructions            = models.TextField(unique=False, default=None, null=True)
    groupId                 = models.CharField(max_length=200, unique=True, default=None)

    def active(self):
        now = datetime.date.today()
        if self.start <= now and now <= self.end:
            return True
        return False

    def soon(self):
        now = datetime.date.today()
        if now <= self.start:
            return True
        return False

class Donation(models.Model):
    user                   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project                = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True) #For Demographics
    thingId                = models.CharField(max_length=200, unique=True, default=None)
    propertyId             = models.JSONField(blank=False, null=True)
    data                   = models.JSONField(blank=False, null=True) #Data this person wants to share
    consent                = models.BooleanField(default=False) # Consent to donate?
    participate                  = models.BooleanField(default=False) # Wants to further participate
    updates                = models.BooleanField(default=False) # Wants to receive updates?
    timestamp              = models.DateTimeField(auto_now_add=True)


class Motivation(models.Model):
    user                   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project                = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    significance           = models.BooleanField(default=False)
    curiosity              = models.BooleanField(default=False)
    researcher             = models.BooleanField(default=False)
    participate            = models.BooleanField(default=False)
    other                  = models.CharField(max_length=300, blank=True, null=True)

class Awareness(models.Model):
    donation               = models.ForeignKey(Donation, on_delete=models.CASCADE)
    awareness              = models.BooleanField(default=False)

class InitialAwareness(models.Model):
    donation            = models.ForeignKey(Donation, on_delete=models.CASCADE)
    collection          = models.BooleanField(default=False)
    takeout             = models.BooleanField(default=False)
    goal                = models.CharField(max_length=200, unique=False, default=None, null=True)