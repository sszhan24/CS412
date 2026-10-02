#models.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Defines the app's data models

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    """A simplified user account with a username, display name, and profile image."""

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        """return string representation"""

        return self.username

    def get_absolute_url(self):
        """return the official url for this profile's detail page."""

        return reverse('mini_insta:show_profile', args=[self.pk])

    def get_all_posts(self):
        """Return all Posts by this Profile, ordered newest first."""

        return self.posts.all().order_by('-timestamp')

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

class Photo(models.Model):
    """An image associated with a Post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        """Return a short description of the Photo."""

        return f"Photo for post {self.post_id}"

class Comment(models.Model):
    """A comment left by one profile on another Profile's Post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  #oldest first
    
    def __str__(self):
        """Return 'Comment by <author> on <post>'."""

        return f"Comment by {self.author.username} on {self.post}"