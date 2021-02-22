from django.db import models

# Create your models here.
class Cause(models.Model):
    title = models.CharField(max_length=100) # Short string frield to hold the name of the cause
    description = models.TextField() # Large string frield to hold a piece of text
    technology = models.CharField(max_length=50) # Short string
    #image = models.FilePathField(path="/img") # Image field, holds the path where the image is stored
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.title
    # Models: classess that represent database tables.