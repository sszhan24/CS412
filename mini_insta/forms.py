#forms.py
#Sion Zhan (sszhan24@bu.edu), 10/1/26
#forms for the mini_insta app

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """form for creating a new Post."""

    image_url = forms.URLField(required=False, label="Photo URL", help_text="Optional: URL of an image to attach to this post.")

    class Meta:
        """Metadata for CreatePostForm"""

        model = Post
        fields = ['caption'] #exclude profile, which is set by the view
    
    def __init__(self, *args, **kwargs):
        """Call parent init, kept explicit for clarity"""

        super().__init__(*args, **kwargs)