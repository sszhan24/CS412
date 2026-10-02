#views.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Defines class based views that get data and delegate the work

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Profile

# Create your views here.

class PostListView(ListView):
    """Display all posts in reverse chronological order"""

    model = Post
    template_name = 'mini_insta/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    """Show a single post along with its comments and author link."""

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class ProfileListView(ListView):
    """List every profile so users can browse accounts."""

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    """Show a profile's bio and all posts authored by that profile."""

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
