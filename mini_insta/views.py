#views.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Defines class based views that get data and delegate the work

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from .models import Profile, Post, Photo
from django.db.models import Q

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

class UpdatePostView(UpdateView):
    """Display a form to update a post's caption, then save it"""

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class DeletePostView(DeleteView):
    """Confirm and delete a post, then redirect to the author's profile"""

    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Add the post and its author's profile to the template context"""

        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        """Redirects to the profile page of the Post's author"""

        post = self.get_object()
        return reverse('mini_insta:show_profile', kwargs={'pk': post.profile.pk})

class ShowFollowersDetailView(DetailView):
    """Display the list of profiles who follow a given profile"""

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    """Display the list of profiles that a given profile is following"""

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class ShowFeedView(DetailView):
    """Display a feed of posts from profiles the given profile follows"""

    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'

class SearchView(ListView):
    """Handle the searching for profiles and posts"""

    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        """Check if a query exists. If not, show the search form"""

        if 'query' not in self.request.GET:
            #no query submitted, show empty search form
            profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
            return render(request, 'mini_insta/search.html', {'profile': profile})

        #query exists, proceed with standard ListView dispatch
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return posts matching the search query"""

        query = self.request.GET.get('query', '')
        if query:
            #filter posts where the caption contains the query
            return Post.objects.filter(caption__icontains=query).order_by('-timestamp')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        """Add the profile, query string, and matching profiles to context"""

        context = super().get_context_data(**kwargs)

        #add the profile
        context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])

        #add the query text
        query = self.request.GET.get('query', '')
        context['query'] = query

        #add matching profiles (searching username, display name, bio)
        if query:
            matching_profiles = Profile.objects.filter(
                Q(username__icontains=query) |
                Q(display_name__icontains=query) |
                Q(bio_text__icontains=query)
            )
            context['profiles'] = matching_profiles
        else:
            context['profiles'] = Profile.objects.none()
        return context