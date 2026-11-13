#dadjokes/admin.py
#Sion Zhan (sszhan24@bu.edu), 11/10/26
#Registers joke and picture with Django admin
#so records can be manipulated through /admin/

from django.contrib import admin
from .models import Joke, Picture

# Register your models here.

@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    """Admin configuration for browsing and editing jokes"""

    list_display = ('text', 'contributor', 'timestamp')

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    """Admin configuration for browsing and editing pictures"""

    list_display = ('image_url', 'contributor', 'timestamp')