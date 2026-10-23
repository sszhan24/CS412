#views.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Defines class based views that get data and delegate the work

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from .models import Profile, Post, Photo, Follow, Like
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

    def get_context_data(self, **kwargs):
        """Add a boolean to check if the logged in user liked this post"""

        context = super().get_context_data(**kwargs)

        has_liked = False
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.filter(user=self.request.user).first()
            if my_profile:
                has_liked = self.object.has_liked(my_profile)

        context['has_liked'] = has_liked
        return context

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

    def get_context_data(self, **kwargs):
        """Add a boolean to check if the logged in user is following this profile"""

        context = super().get_context_data(**kwargs)

        is_following = False

        #check if user is logged in and has a profile
        if self.request.user.is_authenticated:
            #safely fetch the logged in user's profile
            my_profile = Profile.objects.filter(user=self.request.user).first()

            if my_profile:
                #check if my_profile is following the profile being viewed (self.object)
                is_following = my_profile.is_following(self.object)

            context['is_following'] = is_following

        return context

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

class CreateProfileView(CreateView):
    """Display a form to create a user and a profile simultaneously"""

    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        """Add the UserCreationForm to the context"""

        context = super().get_context_data(**kwargs)
        #if re-rendering after a failure, use user_form from kwargs
        #otherwise create blank one
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        """Process both forms, create the user, log them in, and save the profile"""

        #reconstruct the UserCreationForm from POST data
        user_form = UserCreationForm(data=self.request.POST)

        #validate the UserCreationForm
        if user_form.is_valid():
            #save the user and log them in
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

            #attach the new user to the profile instance before saving
            form.instance.user = user

            #delegate to super().form_valid to save the profile and redirect
            return super().form_valid(form)
        else:
            #if the UserCreationForm is invalid (e.g., passwords don't match),
            #re-render the page with errors
            return self.form_invalid(form)

    def form_invalid(self, form, user_form=None):
        """Handle invalid form submission, called by form_valid or default POST"""

        #if user_form wasn't passed in (e.g., profile form itself was invalid on initial submit)
        #recreate it from POST data so it doesn't dissapear
        if user_form is None:
            user_form = UserCreationForm(data=self.request.POST)

        #re-render the template with the form errors attached to the context
        return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

class FollowProfileView(ProfileLoginRequiredMixin, View):
    """Create a follow record where the logged in user follows the target profile"""

    def get(self, request, pk):
        """Handle the GET request to follow a profile"""

        target_profile = get_object_or_404(Profile, pk=pk)
        my_profile = self.get_object() #from the mixin, gets logged in user's profile

        #prevent following yourself
        if my_profile != target_profile:
            #get_or_create prevents duplicate follows if clicked twice
            Follow.objects.get_or_create(profile=target_profile, follower_profile=my_profile)

        return redirect('mini_insta:show_profile', pk=pk)

class UnfollowProfileView(ProfileLoginRequiredMixin, View):
    """Delete a follow record between the logged in user and the target profile"""

    def get(self, request, pk):
        """Handle the GET request to unfollow the profile"""

        target_profile = get_object_or_404(Profile, pk=pk)
        my_profile = self.get_object()

        if my_profile != target_profile:
            #find and delete the follow relation
            Follow.objects.filter(profile=target_profile, follower_profile=my_profile).delete()
        return redirect('mini_insta:show_profile', pk=pk)

class LikePostView(ProfileLoginRequiredMixin, View):
    """Create a like record for a post"""

    def get(self, request, pk):
        """Handle the GET request to like a post"""

        post = get_object_or_404(Post, pk=pk)
        my_profile = self.get_object()

        #prevent liking your own post
        if post.profile != my_profile:
            Like.objects.get_or_create(post=post, profile=my_profile)

        return redirect('mini_insta:show_post', pk=pk)

class UnlikePostView(ProfileLoginRequiredMixin, View):
    """Delete a like record for a post"""

    def get(self, request, pk):
        """Handle the GET request to unlike a post"""

        post = get_object_or_404(Post, pk=pk)
        my_profile = self.get_object()

        if post.profile != my_profile:
            Like.objects.filter(post=post, profile=my_profile).delete()

        return redirect('mini_insta:show_post', pk=pk)