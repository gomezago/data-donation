from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


# Create your models here.
class Project(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title                   = models.CharField(max_length=100, blank=False) # Short string field to hold project name
    description_tweet       = models.CharField(max_length=280, blank=False)  # Tweet-Like description of project
    description             = models.TextField(blank=False)  # Large string frield to hold a piece of text
    hrec                    = models.BooleanField(default=False)
    data                    = models.CharField(max_length=100, blank=False, null=True) #TODO: Array Field
    image                   = models.ImageField(upload_to="images", blank=True, null=True) #TODO: Figure this out
    start                   = models.DateField(blank=False)  # Start of project
    end                     = models.DateField(blank=False)  # End of project
    data_info               = models.TextField(blank=False, null=True)
    groupId                 = models.CharField(max_length=200, unique=True, default=None)

    def active(self):
        now = datetime.date.today()
        if self.start <= now and now <= self.end:
            return True
        return False

class Donation(models.Model):
    user                   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project                = models.ForeignKey('Project', on_delete=models.CASCADE)
    propertyId             = models.CharField(max_length=200, unique=True, default=None)
    updates                = models.BooleanField(default=False)
    timestamp              = models.DateTimeField(auto_now_add=True)