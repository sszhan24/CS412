#urls.py
#Sion Zhan (sszhan24@bu.edu), 9/24/2026
#Description: url patterns/configuration for mini insta app

from django.urls import path
from . import views

app_name = 'mini_insta'

urlpatterns = [
    path('feed/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
]