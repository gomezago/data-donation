from django.db import models

# Create your models here.
class DataSlipDonation(models.Model):
    transport = models.BooleanField(default=False)
    supermarket = models.BooleanField(default=False)
    card = models.BooleanField(default=False)
    wearable = models.BooleanField(default=False)
    apps = models.BooleanField(default=False)