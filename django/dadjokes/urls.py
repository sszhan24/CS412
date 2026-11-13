#dadjokes/urls.py
#Sion Zhan (sszhan24@bu.edu), 11/10/26
#URL patterns for the dadjokes app

from django.urls import path, include
from . import views

app_name = 'dadjokes'

urlpatterns = [
    #HTML Views
    path('', views.random_view, name='random_home'),
    path('random', views.random_view, name='random'),
    path('jokes', views.JokeListView.as_view(), name='joke_list'),
    path('joke/<int:pk>', views.JokeDetailView.as_view(), name='joke_detail'),
    path('pictures', views.PictureListView.as_view(), name='picture_list'),
    path('picture/<int:pk>', views.PictureDetailView.as_view(), name='picture_detail'),

    #API Views
    path('api/', views.JokeRandomAPIView.as_view(), name='api_random_home'),
    path('api/random', views.JokeRandomAPIView.as_view(), name='api_random'),
    path('api/jokes', views.JokeListAPIView.as_view(), name='api_joke_list'),
    path('api/jokes/<int:pk>', views.JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures', views.PictureListAPIView.as_view(), name='api_picture_list'),
    path('api/picture/<int:pk>', views.PictureDetailAPIView.as_view(), name='api_picture_detail'),
    path('api/random_picture', views.PictureRandomAPIView.as_view(), name='api_random_picture'),
]