#dadjokes/serializers.py
#Sion Zhan (sszhan24@bu.edu), 11/10/27
#Serializers for the joke and picture models

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    """A serializer for the joke model"""

    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    """A serializer for the Picture model"""

    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']

