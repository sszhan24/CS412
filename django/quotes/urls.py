# urls.py
# Sion Zhan (sszhan24@bu.edu), 9/10/26
# Description: URL configuration for the quotes app. Defines url patterns for the quotes app, mapping URLs to views.

from django.urls import path
#from django.conf import settings
#from django.conf.urls.static import static #add for static files
from . import views

app_name = 'quotes'

#URL patterns specific to the quotes app:
urlpatterns = [
    path(r'', views.quote, name='Quote of the Day'),
    path(r'show_all', views.show_all, name='Show All'),
    path(r'about', views.about, name='About'),
]


