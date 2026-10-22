#views.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Defines class based views that get data and delegate the work

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from .models import Profile, Post, Photo
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    """A mixin that forces login and automatically finds the logged in user's Profile"""

    def get_login_url(self):
        """Return the URL to the mini_insta login page"""

        return reverse('mini_insta:login')

    def get_object(self):
        """Return the profile associated with the currently logged in user"""

        #self.request.user is the Django user
        #we find the profile where profile.user equals this user
        return get_object_or_404(Profile, user=self.request.user)

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

class CreatePostView(ProfileLoginRequiredMixin, CreateView):
    """Display a form to create a Post for a given Profile, then save it."""

    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    #def get_context_data(self, **kwargs):
    #    """Add the Profile(from the URL pk) to the template context."""

     #   context = super().get_context_data(**kwargs)
    #    context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
        
    #    return context
    
    def form_valid(self, form):
        """Attach the Profile to the Post, then create a Photo if provided."""

        #use the mixin's get_object() to find the logged in user's profile
        form.instance.profile = self.get_object()
        response = super().form_valid(form)
        
        #read uploaded files from request.FILES
        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response
    
    def get_success_url(self):
        """redirect to the newly created Post's detail page."""

        return reverse_lazy('mini_insta:show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(ProfileLoginRequiredMixin, UpdateView):
    """Display a form to update a profile, then save the changes"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class UpdatePostView(LoginRequiredMixin, UpdateView):
    """Display a form to update a post's caption, then save it"""

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_queryset(self):
        """Only allow users to update their own posts"""

        #filter posts so users can only edit posts belonging to their profile
        return Post.objects.filter(profile__user=self.request.user)

class DeletePostView(LoginRequiredMixin, DeleteView):
    """Confirm and delete a post, then redirect to the author's profile"""

    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'

    def get_queryset(self):
        """Only allow the user to delete posts they created"""

        return Post.objects.filter(profile__user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add the post and its author's profile to the template context"""

        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        """Redirects to the profile page of the Post's author"""

        #self.object is still in memory even after it's deleted from the database
        return reverse('mini_insta:show_profile', kwargs={'pk': self.object.profile.pk})

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

class ShowFeedView(ProfileLoginRequiredMixin, DetailView):
    """Display a feed of posts from profiles the given profile follows"""

    model = Profile
    template_name = 'mini_insta/show_feed.html'
    #context_object_name = 'profile'

    #template will still call it "profile" if we add it to get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

class SearchView(ProfileLoginRequiredMixin, ListView):
    """Handle the searching for profiles and posts"""

    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        """Check if a query exists. If not, show the search form"""

        #manually enforce login first
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if 'query' not in self.request.GET:
            #use self.get_object()
            return render(request, 'mini_insta/search.html', {'profile': self.get_object()})

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
        context['profile'] = self.get_object()

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

class MyProfileView(ProfileLoginRequiredMixin, DetailView):
    """Show the logged in user's own profile"""

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class LogoutConfirmationView(TemplateView):
    """Display the logout confirmation page"""

    template_name = 'mini_insta/logged_out.html'