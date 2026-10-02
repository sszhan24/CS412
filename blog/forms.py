#blog/forms.py
#define the forms that we use for create/update/delete operations

from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    """A form to add a Comment to the database."""

    class Meta:
        """associate this form with the comment model; select fields."""

        model = Comment
        fields = ['author', 'text', ]
        #which fields from model should we use

class CreateArticleForm(forms.ModelForm):
    """A form to add an Article to the database."""

    class Meta:
        """associate this form with a model from our database."""

        model = Article
        fields = ['author', 'title', 'text', 'image_url']
