#apps.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Contains MiniInstaConfig, the app's configuration class

from django.apps import AppConfig


class MiniInstaConfig(AppConfig):
    """App configuration for mini_insta"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_insta'
