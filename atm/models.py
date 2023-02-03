from django.db import models

# Create your models here.
class DataSlipDonation(models.Model):
    transport = models.BooleanField(default=False)
    supermarket = models.BooleanField(default=False)
    card = models.BooleanField(default=False)
    wearable = models.BooleanField(default=False)
    apps = models.BooleanField(default=False)

class DataSlipFeedback(models.Model):
    reaction = models.IntegerField()
    action = models.TextField(blank=False, null=True)  # Large string frield to hold a piece of text