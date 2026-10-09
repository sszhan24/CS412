#views.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Defines class based views that get data and delegate the work

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import CreatePostForm, UpdateProfileForm
from .models import Profile, Post, Photo

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

class CreatePostView(CreateView):
    """Display a form to create a Post for a given Profile, then save it."""

    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        """Add the Profile(from the URL pk) to the template context."""

        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
        
        return context
    
    def form_valid(self, form):
        """Attach the Profile to the Post, then create a Photo if provided."""

        #attach the Profile FK before saving the Post
        form.instance.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        response = super().form_valid(form)

        #if user provided image URL, create a Photo for the Post
        #image_url = form.cleaned_data.get('image_url')
        #if image_url:
        #    Photo.objects.create(post=self.object, image_url=image_url)
        
        #read uploaded files from request.FILES
        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response
    
    def get_success_url(self):
        """redirect to the newly created Post's detail page."""

        return reverse_lazy('mini_insta:show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(UpdateView):
    """Display a form to update a profile, then save the changes"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'