#mini_insta/serializers.py
#Sion Zhan (sszhan24@bu.edu), 11/17/26
#Serializerss for the mini_insta REST API

from rest_framework import serializers
from .models import Profile, Post, Photo, Comment

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model"""

    class Meta:
        """Metadata for ProfileSerializer"""

        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text']

class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for the Photo model"""

    class Meta:
        """Metadata for PhotoSerializer"""

        model = Photo
        fields = ['id', 'image_url', 'image_file']

class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model"""

    #Include the author's username so React doesn't have to look it up
    author_username = serializers.ReadOnlyField(source='profile.username')
    #Include a list of photos for this post
    photos = PhotoSerializer(source='get_all_photos', many=True, read_only=True)

    class Meta:
        """Metadata for PostSerializer"""
        
        model = Post
        fields = ['id', 'profile', 'author_username', 'caption', 'timestamp', 'photos']