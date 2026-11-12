#blog/serializers.py
#Serializers convert our django data models to a 
#text-representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    """A serializer for the article model. Specify which model/fields to send in the API"""

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'text', 'published', 'image_file']

    #add methods to customize the Create/Read/Update/Delete operations
    def create(self, validated_data):
        """Override the superclass method that handles object creation"""

        print(f'ArticleSerializer.create, validated_data={validated_data}.')
        #create an article object
        article = Article(**validated_data)
        #attach a FK for the User
        article.user = User.objects.first()
        #save the object to the database
        article.save()
        #return an object instance
        return article