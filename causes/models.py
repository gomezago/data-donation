from django.db import models

# Create your models here.
class Cause(models.Model):
    title = models.CharField(max_length=100, blank=False) # Short string frield to hold the name of the cause
    description_tweet = models.CharField(max_length=280, blank=False, null=True) #Tweet-Like description of project
    description = models.TextField(blank=False, null=True) # Large string frield to hold a piece of text
    data = models.CharField(max_length=100, blank=False) # Short string
    image = models.ImageField(upload_to="images", blank=True)
    active = models.BooleanField(default=False) # Status: Accepting data or not
    start = models.DateField(blank=False, null=True) # Start of project
    end = models.DateField(blank=False, null=True) # End of project
    contact_name = models.CharField(max_length=100, blank=False, null=True) #Name of Researcher
    contact_email = models.EmailField(blank=False, null=True) # Email of person in charge.

    def __str__(self):
        return self.title
    # Models: classess that represent database tables.

class Donation(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=255, blank=False)
    data = models.ImageField(blank=True, upload_to="data/%Y/%m/%d") # Should this be FileField?
    available = models.BooleanField(default=False) # Participate in further studies?
    timestamp = models.DateTimeField(auto_now_add=True) #Assigns time and data when instance of class is saved
    cause = models.ForeignKey('Cause', on_delete=models.PROTECT) # Many to one relationship

    def __str__(self):
        return self.timestamp.strftime("%m/%d/%Y_%H:%M:%S")
