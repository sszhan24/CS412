#admin.py
#Sion Zhan (sszhan24@bu.edu), 9/30/26
#Registers Profile, Post, and Comment with Django admin
#so records can be manipulated through /admin/


from django.contrib import admin
from .models import Profile, Post, Comment, Photo

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for browsing and editing Profiles."""

    list_display = ('username', 'display_name', 'join_date')
    search_fields = ('username', 'display_name')

class CommentInline(admin.TabularInline):
    """Allow comments to be edited inline on a Post's admin page."""

    model = Comment
    extra = 1

class PhotoInline(admin.TabularInline):
    """Allow photos to be edited inline on a Post's admin page."""

    model = Photo
    extra = 1
    fields = ('image_url', 'image_file', 'timestamp')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Posts, with inline comments."""

    list_display = ('__str__', 'profile', 'timestamp')
    list_filter = ('profile', 'timestamp')
    search_fields = ('caption',)
    inlines = [PhotoInline, CommentInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Admin configuration for browsing Photos directly."""

    list_display = ('__str__', 'post', 'timestamp')
    list_filter = ('post',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for browsing comments directly."""

    list_display = ('author', 'post', 'created_at')
    list_filter = ('author',)
