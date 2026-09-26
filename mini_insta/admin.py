from django.contrib import admin
from .models import Profile, Post, Comment

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for browsing and editing Profiles."""

    list_display = ('username', 'display_name', 'join_date')
    search_fields = ('username', 'display_name')

class CommentInLine(admin.TabularInline):
    """Allow comments to be edited inline on a Post's admin page."""

    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Posts, with inline comments."""

    list_display = ('__str__', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('caption',)
    inlines = [CommentInLine]
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for browsing comments directly."""

    list_display = ('author', 'post', 'created_at')
    list_filter = ('author',)
