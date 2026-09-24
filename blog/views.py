#from django.shortcuts import render
from .models import Article
from django.views.generic import ListView

# Create your views here.

class ShowAllView(ListView):
    """create a subclass of ListView to display all blog articles."""

    model = Article #retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #how to find data in the template file
