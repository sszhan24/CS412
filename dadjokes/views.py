#dadjokes/views.py
#Sion Zhan (sszhan24@bu.edu), 11/10/26
#Views for the dadjokes app: HTML pages and REST API

from django.shortcuts import render, get_object_or_404
import random
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework import generics
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer

# Create your views here.

# HTML Views

def random_view(request):
    """Show one random joke and one random picture"""

    jokes = Joke.objects.all()
    pictures = Picture.objects.all()
    joke = random.choice(jokes) if jokes else None
    picture = random.choice(pictures) if pictures else None

    return render(request, 'dadjokes/random.html', {
        'joke': joke,
        'picture': picture,
    })

class JokeListView(ListView):
    """Show a page with all jokes, no images"""

    model = Joke
    template_name = 'dadjokes/joke_list.html'
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    """Show one joke by its primary key"""

    model = Joke
    template_name = 'dadjokes/joke_detail.html'
    context_object_name = 'joke'

class PictureListView(ListView):
    """Show a page with all pictures, no jokes"""

    model = Picture
    template_name = 'dadjokes/picture_list.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    """Show one picture by its primary key"""

    model = Picture
    template_name = 'dadjokes/picture_detail.html'
    context_object_name = 'picture'

# API Views

class JokeRandomAPIView(generics.RetrieveAPIView):
    """Return a JSON representation of one random joke"""

    serializer_class = JokeSerializer

    def get_object(self):
        """choose a random joke out of all the options"""

        return random.choice(Joke.objects.all())

class JokeListAPIView(generics.ListCreateAPIView):
    """Return all jokes as JSON; accepts POST to create a new joke"""

    queryset = Joke.objects.all().order_by('-timestamp')
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    """Return one joke by primary key as JSON"""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    """Return all picutres as JSON"""

    queryset = Picture.objects.all().order_by('-timestamp')
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    """Return one picture by primary key as JSON"""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureRandomAPIView(generics.RetrieveAPIView):
    """Return a JSON representation of one picture"""

    serializer_class = PictureSerializer

    def get_object(self):
        """choose a random picture out of all the options"""

        return random.choice(Picture.objects.all())