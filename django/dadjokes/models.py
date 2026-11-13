#dadjokes/models.py
#Sion Zhan (sszhan24@bu.edu), 11/10/26
#defines the joke and picture models for the dadjokes app

from django.db import models

# Create your models here.

class Joke(models.Model):
    """A dad joke submitted by a contributor"""

    text = models.TextField()
    contributor = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a short preview of the joke"""

        return f"{self.text[:50]} (by {self.contributor})"

class Picture(models.Model):
    """A silly image/GIF submitted by a contributor, independent of the joke"""

    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a short caption/description of the picture"""

        return f"Picture by {self.contributor}"