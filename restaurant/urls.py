#urls.py
#Name: Sion Zhan (sszhan24@bu.edu), 9/17/2026
#Description: URL patterns for the restaurant app.

from django.urls import path
from . import views

urlpatterns = [
    path('main', views.main, name='main'),
    path('order', views.order, name='order'),
    path('confirmation', views.confirmation, name='confirmation'),
]