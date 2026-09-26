#urls.py

from django.urls import path
from .views import ShowAllView, ArticleView, RandomArticleView #our view class definition

urlpatterns = [
    #map URL (empty string) to the view
    path('article/<int:pk>', ArticleView.as_view(), name='article'), #show one article
    path('random', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('', ShowAllView.as_view(), name='blog_home'),
]