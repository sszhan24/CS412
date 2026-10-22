#models.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Defines the app's data models

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """A simplified user account with a username, display name, and profile image."""

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """return string representation"""

        return self.username

    def get_absolute_url(self):
        """return the official url for this profile's detail page."""

        return reverse('mini_insta:show_profile', args=[self.pk])

    def get_all_posts(self):
        """Return all Posts by this Profile, ordered newest first."""

        return self.posts.all().order_by('-timestamp')

    #follow accessors
    def get_followers(self):
        """Return a list of profiles who follow this profile"""

        #follows where this profile is the one being followed
        follows = Follow.objects.filter(profile=self)
        #extract the follower profile from each
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        """Return the number of profiles following this profile"""

        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Return a list of profiles this profile is following"""

        #follows where this profile is the one doing the following
        follows = Follow.objects.filter(follower_profile=self)
        #extract the followed profile from each
        return [f.profile for f in follows]

    def get_num_following(self):
        """Return the number of profiles this profile is following"""

        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        """Return posts from all profiles this profile follows, newest first"""

        #get the profiles this user follows
        followed_profiles = self.get_following()

        #filter posts whose author is in that list, newest first
        return Post.objects.filter(profile__in=followed_profiles).order_by('-timestamp')

class Post(models.Model):
    """An IG post: a caption by a Profile, containing one or more Photos."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    #author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    #caption = models.TextField(blank=True)
    #image_url = models.URLField(blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']   #newest first
    
    def __str__(self):
        """return string representation"""

        return f"{self.profile.username}: {self.caption[:30]}"

    def get_absolute_url(self):
        """return the actual URL for this post's detail page."""

        return reverse('mini_insta:show_post', args=[self.pk])

    def get_all_photos(self):
        """Return all Photos attached to this Post, ordered oldest first."""

        return self.photos.all().order_by('timestamp')

    def get_all_comments(self):
        """Return all comments on this post, oldest first"""

        return Comment.objects.filter(post=self).order_by('timestamp')

    def get_likes(self):
        """Return all likes on this post"""

        return Like.objects.filter(post=self)

class Photo(models.Model):
    """An image associated with a Post. Stored either as URL or uploaded file"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(blank=True)
    image_file = models.FileField(upload_to='mini_insta/photos/', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        """Return a short description of the Photo."""

        if self.image_url:
            return f"Photo (URL) for post {self.post_id}"
        elif self.image_file:
            return f"Photo (file: {self.image_file.name}) for post {self.post_id}"

        return f"Photo (empty) for post {self.post_id}"

    def get_image_url(self):
        """Return the URL for this Photo, prefers image_url over image_file."""

        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
            
        return ''

class Comment(models.Model):
    """A comment left by one profile on another Profile's Post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']  #oldest first
    
    def __str__(self):
        """Return 'Comment by <author> on <post>'."""

        return f"Comment by {self.profile.username} on {self.post}"

class Follow(models.Model):
    """A one directional follow relation between two profiles"""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return '<follower> follows <profile>'"""

        return f"{self.follower_profile.username} follows {self.profile.username}"

class Like(models.Model):
    """A like on a post by a profile"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return '<profile> likes post <id>'"""

        return f"{self.profile.username} likes post {self.post_id}"
