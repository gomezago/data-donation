from django.db import models

# Create your models here.
class Cause(models.Model):
    title = models.CharField(max_length=100) # Short string frield to hold the name of the cause
    description = models.TextField() # Large string frield to hold a piece of text
    technology = models.CharField(max_length=20) # Short string
    image = models.FilePathField(path="/img") # Image field, holds the path where the image is stored

    # Models: classess that represent database tables.