from django.db import models
from .managers import BucketUserManager

# Create your models here.
class BucketUser(models.Model):
    objects = BucketUserManager()

    id = models.CharField(primary_key=True, max_length=100)
    email = models.EmailField()
    email_verified = models.BooleanField()
    name = models.TextField()
    username = models.TextField()
    sid = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True)