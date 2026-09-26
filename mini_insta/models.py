from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    """A simplified user account: just a username and a bio"""

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    profile_img_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        """return string representation"""

        return self.username

    def get_absolute_url(self):
        """return the official url for this profile's detail page."""

        return reverse('mini_insta:profile-detail', args=[self.pk])

class Post(models.Model):
    """An image and caption posted by a profile"""

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']   #newest first
    
    def __str__(self):
        """return string representation"""

        return f"{self.author.username}: {self.caption[:30]}"

    def get_absolute_url(self):
        """return the actual URL for this post's detail page."""

        return reverse('mini_insta:post-detail', args=[self.pk])

class Comment(models.Model):
    """A comment left by one profile on another Profile's Post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  #oldest first
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"